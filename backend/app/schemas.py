from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from .models import UserRole


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores/hyphens allowed)")
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be 3-50 characters")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: "UserOut"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
    is_banned: bool
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Albums ────────────────────────────────────────────────────────────────────

class SongOut(BaseModel):
    id: int
    title: str
    track_number: int
    duration: Optional[str] = None
    audio_url: Optional[str] = None
    youtube_url: Optional[str] = None
    youtube_embed_id: Optional[str] = None
    is_premium: bool
    play_count: int

    class Config:
        from_attributes = True


class AlbumOut(BaseModel):
    id: int
    title: str
    year: int
    cover_url: Optional[str] = None
    description: Optional[str] = None
    is_premium: bool
    spotify_url: Optional[str] = None
    songs: List[SongOut] = []

    class Config:
        from_attributes = True


class AlbumCreate(BaseModel):
    title: str
    year: int
    cover_url: Optional[str] = None
    description: Optional[str] = None
    is_premium: bool = False
    spotify_url: Optional[str] = None


class SongCreate(BaseModel):
    album_id: int
    title: str
    track_number: int
    duration: Optional[str] = None
    audio_url: Optional[str] = None
    youtube_url: Optional[str] = None
    youtube_embed_id: Optional[str] = None
    lyrics: Optional[str] = None
    is_premium: bool = False


# ── Admin ─────────────────────────────────────────────────────────────────────

class UserAdminUpdate(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_banned: Optional[bool] = None
    ban_reason: Optional[str] = None


class UserAdminOut(UserOut):
    ban_reason: Optional[str] = None

    class Config:
        from_attributes = True


# ── Contact ───────────────────────────────────────────────────────────────────

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Beats ─────────────────────────────────────────────────────────────────────

class BeatCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    tags: Optional[str] = None
    bpm: Optional[int] = None
    musical_key: Optional[str] = None
    price: float = 0.0
    image_url: Optional[str] = None
    audio_preview_url: Optional[str] = None
    is_available: bool = True
    is_exclusive: bool = False

class BeatOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: str
    tags: Optional[str] = None
    bpm: Optional[int] = None
    musical_key: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    audio_preview_url: Optional[str] = None
    is_available: bool
    is_exclusive: bool
    play_count: int
    created_at: datetime

    class Config:
        from_attributes = True
