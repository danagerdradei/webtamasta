from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import require_admin

router = APIRouter(prefix="/api/services", tags=["services"])

SERVICE_CATEGORY_LABELS = {
    "vocal_recording": "Captación de Voces",
    "beat_creation": "Creación de Beats",
    "mixing": "Mezcla",
    "mastering": "Masterización",
    "multimedia": "Multimedia",
    "equipment_rental": "Alquiler de Equipos",
    "mobile_recording": "Grabación Móvil",
}


@router.get("/categories")
def get_categories():
    return [{"value": k, "label": v} for k, v in SERVICE_CATEGORY_LABELS.items()]


@router.get("", response_model=List[schemas.ServiceOut])
def list_services(active_only: bool = True, db: Session = Depends(get_db)):
    q = db.query(models.Service)
    if active_only:
        q = q.filter(models.Service.is_active == True)
    return q.order_by(models.Service.sort_order, models.Service.id).all()


@router.get("/{service_id}", response_model=schemas.ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc


@router.post("", response_model=schemas.ServiceOut)
def create_service(body: schemas.ServiceCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    svc = models.Service(**body.model_dump())
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc


@router.put("/{service_id}", response_model=schemas.ServiceOut)
def update_service(service_id: int, body: schemas.ServiceCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    svc = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    for k, v in body.model_dump().items():
        setattr(svc, k, v)
    db.commit()
    db.refresh(svc)
    return svc


@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    svc = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(svc)
    db.commit()
    return {"ok": True}


# ── Packages ──────────────────────────────────────────────────────────────────

@router.get("/packages/all", response_model=List[schemas.ServicePackageOut])
def list_packages(active_only: bool = True, db: Session = Depends(get_db)):
    q = db.query(models.ServicePackage)
    if active_only:
        q = q.filter(models.ServicePackage.is_active == True)
    return q.order_by(models.ServicePackage.is_featured.desc(), models.ServicePackage.id).all()


@router.post("/packages", response_model=schemas.ServicePackageOut)
def create_package(body: schemas.ServicePackageCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    pkg = models.ServicePackage(**body.model_dump())
    db.add(pkg)
    db.commit()
    db.refresh(pkg)
    return pkg


@router.put("/packages/{pkg_id}", response_model=schemas.ServicePackageOut)
def update_package(pkg_id: int, body: schemas.ServicePackageCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    pkg = db.query(models.ServicePackage).filter(models.ServicePackage.id == pkg_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    for k, v in body.model_dump().items():
        setattr(pkg, k, v)
    db.commit()
    db.refresh(pkg)
    return pkg


@router.delete("/packages/{pkg_id}")
def delete_package(pkg_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    pkg = db.query(models.ServicePackage).filter(models.ServicePackage.id == pkg_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    db.delete(pkg)
    db.commit()
    return {"ok": True}
