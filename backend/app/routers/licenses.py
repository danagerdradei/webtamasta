from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import datetime

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_admin

router = APIRouter(prefix="/api/licenses", tags=["licenses"])


def generate_license_number() -> str:
    return f"LT-{datetime.datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:8].upper()}"


@router.get("/", response_model=List[schemas.LicenseOut])
def list_licenses(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    q = db.query(models.License)
    if status:
        try:
            q = q.filter(models.License.status == models.LicenseStatus(status))
        except ValueError:
            pass
    return q.order_by(models.License.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{license_id}", response_model=schemas.LicenseOut)
def get_license(
    license_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    lic = db.query(models.License).filter(models.License.id == license_id).first()
    if not lic:
        raise HTTPException(status_code=404, detail="License not found")
    return lic


@router.get("/verify/{license_number}", response_model=schemas.LicenseOut)
def verify_license(license_number: str, db: Session = Depends(get_db)):
    """Public endpoint to verify a license by number."""
    lic = db.query(models.License).filter(models.License.license_number == license_number).first()
    if not lic:
        raise HTTPException(status_code=404, detail="License not found")
    return lic


@router.post("/", response_model=schemas.LicenseOut, status_code=status.HTTP_201_CREATED)
def create_license(
    data: schemas.LicenseCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    beat_title = data.beat_title
    if data.beat_id and not beat_title:
        beat = db.query(models.Beat).filter(models.Beat.id == data.beat_id).first()
        if beat:
            beat_title = beat.title

    lic = models.License(
        license_number=generate_license_number(),
        beat_id=data.beat_id,
        client_name=data.client_name,
        client_email=data.client_email,
        beat_title=beat_title,
        license_type=data.license_type,
        price_paid=data.price_paid,
        expiry_date=data.expiry_date,
        terms=data.terms,
        notes=data.notes,
    )
    db.add(lic)
    db.commit()
    db.refresh(lic)
    return lic


@router.patch("/{license_id}", response_model=schemas.LicenseOut)
def update_license(
    license_id: int,
    data: schemas.LicenseAdminUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    lic = db.query(models.License).filter(models.License.id == license_id).first()
    if not lic:
        raise HTTPException(status_code=404, detail="License not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lic, field, value)
    db.commit()
    db.refresh(lic)
    return lic


@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(
    license_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    lic = db.query(models.License).filter(models.License.id == license_id).first()
    if not lic:
        raise HTTPException(status_code=404, detail="License not found")
    db.delete(lic)
    db.commit()
