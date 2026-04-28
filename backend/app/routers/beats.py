from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..auth import require_admin

router = APIRouter(prefix="/api/beats", tags=["beats"])

HIPHOP_CATEGORIES = [
    "Boom Bap", "Trap", "Drill", "UK Drill", "Phonk", "Lo-Fi Hip-Hop",
    "G-Funk", "East Coast", "West Coast", "Southern / Dirty South",
    "Cloud Rap", "Emo Rap / Sad Rap", "Latin Trap", "Afro Trap",
    "R&B / Neo Soul", "Jazz Rap", "Golden Era / Old School",
    "Underground / Conscious", "Gangsta Rap", "Melodic Rap",
    "Experimental / Abstract", "Detroit Hip-Hop", "Memphis Rap",
    "Hyphy", "Crunk", "Instrumental Hip-Hop", "New School", "Afrobeats Fusion",
]

@router.get("/categories")
def get_categories():
    return HIPHOP_CATEGORIES

@router.get("", response_model=List[schemas.BeatOut])
def list_beats(
    q: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    available_only: bool = Query(True),
    db: Session = Depends(get_db),
):
    query = db.query(models.Beat)
    if available_only:
        query = query.filter(models.Beat.is_available == True)
    if category:
        query = query.filter(models.Beat.category == category)
    if q:
        like = f"%{q.lower()}%"
        query = query.filter(
            models.Beat.title.ilike(like) |
            models.Beat.tags.ilike(like) |
            models.Beat.description.ilike(like)
        )
    return query.order_by(models.Beat.created_at.desc()).all()

@router.get("/{beat_id}", response_model=schemas.BeatOut)
def get_beat(beat_id: int, db: Session = Depends(get_db)):
    beat = db.query(models.Beat).filter(models.Beat.id == beat_id).first()
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    return beat

@router.post("", response_model=schemas.BeatOut, status_code=201)
def create_beat(
    payload: schemas.BeatCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    beat = models.Beat(**payload.model_dump())
    db.add(beat)
    db.commit()
    db.refresh(beat)
    return beat

@router.put("/{beat_id}", response_model=schemas.BeatOut)
def update_beat(
    beat_id: int,
    payload: schemas.BeatCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    beat = db.query(models.Beat).filter(models.Beat.id == beat_id).first()
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    for k, v in payload.model_dump().items():
        setattr(beat, k, v)
    db.commit()
    db.refresh(beat)
    return beat

@router.delete("/{beat_id}", status_code=204)
def delete_beat(
    beat_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    beat = db.query(models.Beat).filter(models.Beat.id == beat_id).first()
    if not beat:
        raise HTTPException(status_code=404, detail="Beat not found")
    db.delete(beat)
    db.commit()

@router.post("/{beat_id}/play")
def increment_play(beat_id: int, db: Session = Depends(get_db)):
    beat = db.query(models.Beat).filter(models.Beat.id == beat_id).first()
    if beat:
        beat.play_count += 1
        db.commit()
    return {"ok": True}
