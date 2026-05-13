from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..auth import require_admin, get_current_user

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("", response_model=schemas.BookingOut)
def create_booking(body: schemas.BookingCreate, db: Session = Depends(get_db)):
    booking = models.Booking(**body.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("", response_model=List[schemas.BookingOut])
def list_bookings(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    q = db.query(models.Booking)
    if status:
        q = q.filter(models.Booking.status == status)
    return q.order_by(models.Booking.booking_date.desc()).all()


@router.get("/{booking_id}", response_model=schemas.BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    b = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    return b


@router.patch("/{booking_id}", response_model=schemas.BookingOut)
def update_booking(booking_id: int, body: schemas.BookingAdminUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    b = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(b, k, v)
    db.commit()
    db.refresh(b)
    return b


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    b = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(b)
    db.commit()
    return {"ok": True}
