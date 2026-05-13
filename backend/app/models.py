from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, Float,
    ForeignKey, Enum as SAEnum, func
)
from sqlalchemy.orm import relationship
import enum
from .database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    premium = "premium"
    free = "free"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.free, nullable=False)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    cover_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    is_premium = Column(Boolean, default=False)
    spotify_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    songs = relationship("Song", back_populates="album", cascade="all, delete-orphan")


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    title = Column(String(200), nullable=False)
    track_number = Column(Integer, nullable=False)
    duration = Column(String(10), nullable=True)
    audio_url = Column(String(500), nullable=True)
    youtube_url = Column(String(500), nullable=True)
    youtube_embed_id = Column(String(50), nullable=True)
    lyrics = Column(Text, nullable=True)
    is_premium = Column(Boolean, default=False)
    play_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    album = relationship("Album", back_populates="songs")


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Beat(Base):
    __tablename__ = "beats"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    tags = Column(String(500), nullable=True)
    bpm = Column(Integer, nullable=True)
    musical_key = Column(String(30), nullable=True)
    price = Column(Float, default=0.0)
    image_url = Column(String(500), nullable=True)
    audio_preview_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True)
    is_exclusive = Column(Boolean, default=False)
    play_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Studio models ──────────────────────────────────────────────────────────────

class ServiceCategory(str, enum.Enum):
    vocal_recording = "vocal_recording"
    beat_creation = "beat_creation"
    mixing = "mixing"
    mastering = "mastering"
    multimedia = "multimedia"
    equipment_rental = "equipment_rental"
    mobile_recording = "mobile_recording"


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(SAEnum(ServiceCategory), nullable=False)
    price_from = Column(Float, nullable=True)
    duration_hours = Column(Float, nullable=True)
    image_url = Column(String(500), nullable=True)
    features = Column(Text, nullable=True)  # JSON array as string
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookings = relationship("Booking", back_populates="service")


class ServicePackage(Base):
    __tablename__ = "service_packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    services_included = Column(Text, nullable=True)  # JSON array as string
    original_price = Column(Float, default=0.0)
    discounted_price = Column(Float, default=0.0)
    discount_pct = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    daily_rate = Column(Float, default=0.0)
    weekly_rate = Column(Float, default=0.0)
    deposit_amount = Column(Float, default=0.0)
    image_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True)
    quantity_total = Column(Integer, default=1)
    quantity_available = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(100), nullable=False)
    client_phone = Column(String(30), nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    service_type = Column(String(100), nullable=True)
    booking_date = Column(DateTime(timezone=True), nullable=False)
    duration_hours = Column(Float, default=1.0)
    status = Column(SAEnum(BookingStatus), default=BookingStatus.pending)
    notes = Column(Text, nullable=True)
    total_price = Column(Float, default=0.0)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="bookings")
    service = relationship("Service", back_populates="bookings")


class LicenseType(str, enum.Enum):
    basic = "basic"           # Non-exclusive, limited use
    standard = "standard"     # Non-exclusive, broader use
    exclusive = "exclusive"   # Full exclusive rights
    sync = "sync"             # Sync/video use
    custom = "custom"         # Custom terms


class LicenseStatus(str, enum.Enum):
    active = "active"
    expired = "expired"
    revoked = "revoked"
    pending = "pending"


class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String(50), unique=True, nullable=False, index=True)
    beat_id = Column(Integer, ForeignKey("beats.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(100), nullable=False)
    beat_title = Column(String(200), nullable=True)
    license_type = Column(SAEnum(LicenseType), default=LicenseType.basic)
    status = Column(SAEnum(LicenseStatus), default=LicenseStatus.active)
    price_paid = Column(Float, default=0.0)
    issued_date = Column(DateTime(timezone=True), server_default=func.now())
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    terms = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    beat = relationship("Beat", backref="licenses")
    user = relationship("User", backref="licenses")
