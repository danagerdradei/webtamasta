from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user, require_admin

router = APIRouter(prefix="/api/albums", tags=["albums"])


@router.get("", response_model=List[schemas.AlbumOut])
def list_albums(db: Session = Depends(get_db)):
    albums = db.query(models.Album).order_by(models.Album.year.desc()).all()
    for album in albums:
        if album.is_premium:
            album.songs = []
    return albums


@router.get("/songs", response_model=List[schemas.SongOut])
def list_all_songs(db: Session = Depends(get_db)):
    return db.query(models.Song).order_by(models.Song.album_id, models.Song.track_number).all()


@router.get("/search")
def search_songs(
    q: str = "",
    db: Session = Depends(get_db),
):
    if not q or len(q) < 1:
        return []
    query = f"%{q.lower()}%"
    songs = (
        db.query(models.Song)
        .join(models.Album)
        .filter(models.Song.title.ilike(query))
        .limit(30)
        .all()
    )
    results = []
    for song in songs:
        album = db.query(models.Album).filter(models.Album.id == song.album_id).first()
        results.append({
            "id": song.id,
            "title": song.title,
            "track_number": song.track_number,
            "duration": song.duration,
            "youtube_embed_id": song.youtube_embed_id,
            "audio_url": song.audio_url,
            "is_premium": song.is_premium,
            "play_count": song.play_count,
            "album_id": song.album_id,
            "album_title": album.title if album else "",
            "album_cover": album.cover_url if album else "",
            "album_year": album.year if album else 0,
        })
    return results


@router.get("/{album_id}", response_model=schemas.AlbumOut)
def get_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user),
):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    if album.is_premium:
        if not current_user or current_user.role not in (models.UserRole.premium, models.UserRole.admin):
            album_dict = {
                "id": album.id, "title": album.title, "year": album.year,
                "cover_url": album.cover_url, "description": album.description,
                "is_premium": album.is_premium, "spotify_url": album.spotify_url,
                "songs": [],
            }
            return album_dict
    return album


@router.post("", response_model=schemas.AlbumOut, status_code=201)
def create_album(
    payload: schemas.AlbumCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    album = models.Album(**payload.model_dump())
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


@router.put("/{album_id}", response_model=schemas.AlbumOut)
def update_album(
    album_id: int,
    payload: schemas.AlbumCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    for k, v in payload.model_dump().items():
        setattr(album, k, v)
    db.commit()
    db.refresh(album)
    return album


@router.delete("/{album_id}", status_code=204)
def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    db.delete(album)
    db.commit()


@router.post("/songs", response_model=schemas.SongOut, status_code=201)
def create_song(
    payload: schemas.SongCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    song = models.Song(**payload.model_dump())
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


@router.post("/songs/{song_id}/play")
def increment_play(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if song:
        song.play_count += 1
        db.commit()
    return {"ok": True}
