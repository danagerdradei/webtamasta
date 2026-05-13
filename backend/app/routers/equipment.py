from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import require_admin

router = APIRouter(prefix="/api/equipment", tags=["equipment"])

EQUIPMENT_CATEGORIES = [
    "Micrófonos", "Interfaces de Audio", "Monitores", "Auriculares",
    "Controladores MIDI", "Instrumentos", "Procesadores / Outboard",
    "Cables y Accesorios", "Iluminación", "Cámaras / Video",
]


@router.get("/categories")
def get_categories():
    return EQUIPMENT_CATEGORIES


@router.get("", response_model=List[schemas.EquipmentOut])
def list_equipment(available_only: bool = False, db: Session = Depends(get_db)):
    q = db.query(models.Equipment)
    if available_only:
        q = q.filter(models.Equipment.is_available == True)
    return q.order_by(models.Equipment.category, models.Equipment.name).all()


@router.get("/{eq_id}", response_model=schemas.EquipmentOut)
def get_equipment(eq_id: int, db: Session = Depends(get_db)):
    eq = db.query(models.Equipment).filter(models.Equipment.id == eq_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return eq


@router.post("", response_model=schemas.EquipmentOut)
def create_equipment(body: schemas.EquipmentCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    eq = models.Equipment(**body.model_dump())
    db.add(eq)
    db.commit()
    db.refresh(eq)
    return eq


@router.put("/{eq_id}", response_model=schemas.EquipmentOut)
def update_equipment(eq_id: int, body: schemas.EquipmentCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    eq = db.query(models.Equipment).filter(models.Equipment.id == eq_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    for k, v in body.model_dump().items():
        setattr(eq, k, v)
    db.commit()
    db.refresh(eq)
    return eq


@router.delete("/{eq_id}")
def delete_equipment(eq_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    eq = db.query(models.Equipment).filter(models.Equipment.id == eq_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db.delete(eq)
    db.commit()
    return {"ok": True}
