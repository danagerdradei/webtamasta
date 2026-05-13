from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=List[schemas.UserAdminOut])
def list_users(
    role: Optional[str] = None,
    banned: Optional[bool] = None,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    q = db.query(models.User)
    if role:
        q = q.filter(models.User.role == role)
    if banned is not None:
        q = q.filter(models.User.is_banned == banned)
    return q.order_by(models.User.created_at.desc()).all()


@router.patch("/users/{user_id}", response_model=schemas.UserAdminOut)
def update_user(
    user_id: int,
    payload: schemas.UserAdminUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(require_admin),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot modify your own admin account")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(require_admin),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    db.delete(user)
    db.commit()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    return {
        "total_users": db.query(models.User).count(),
        "premium_users": db.query(models.User).filter(models.User.role == models.UserRole.premium).count(),
        "free_users": db.query(models.User).filter(models.User.role == models.UserRole.free).count(),
        "banned_users": db.query(models.User).filter(models.User.is_banned == True).count(),
        "total_albums": db.query(models.Album).count(),
        "total_songs": db.query(models.Song).count(),
        "total_messages": db.query(models.ContactMessage).count(),
        "unread_messages": db.query(models.ContactMessage).filter(models.ContactMessage.is_read == False).count(),
        "total_services": db.query(models.Service).count(),
        "total_equipment": db.query(models.Equipment).count(),
        "total_bookings": db.query(models.Booking).count(),
        "pending_bookings": db.query(models.Booking).filter(models.Booking.status == models.BookingStatus.pending).count(),
        "total_packages": db.query(models.ServicePackage).count(),
        "total_licenses": db.query(models.License).count(),
        "active_licenses": db.query(models.License).filter(models.License.status == models.LicenseStatus.active).count(),
    }


@router.get("/messages", response_model=List[schemas.ContactOut])
def list_messages(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    return db.query(models.ContactMessage).order_by(models.ContactMessage.created_at.desc()).all()


@router.patch("/messages/{msg_id}/read", response_model=schemas.ContactOut)
def mark_read(
    msg_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    msg = db.query(models.ContactMessage).filter(models.ContactMessage.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.is_read = True
    db.commit()
    db.refresh(msg)
    return msg
