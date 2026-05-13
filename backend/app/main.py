from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import engine, Base
from .config import settings
from .routers import auth, albums, admin, contact, beats, services, equipment, bookings, licenses
from . import models


def seed_initial_data():
    import datetime, json
    from sqlalchemy.orm import Session
    from .auth import hash_password

    with Session(engine) as db:

        # ── Users ──────────────────────────────────────────────────────────────
        if not db.query(models.User).filter(models.User.email == settings.ADMIN_EMAIL).first():
            db.add(models.User(
                username="latintunes_admin",
                email=settings.ADMIN_EMAIL,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                role=models.UserRole.admin,
            ))
            db.commit()
            print(f"[seed] Admin created: {settings.ADMIN_EMAIL}")

        if not db.query(models.User).filter(models.User.email == "visitante@latintunes.com").first():
            db.add(models.User(
                username="visitante",
                email="visitante@latintunes.com",
                hashed_password=hash_password("Visitante@123"),
                role=models.UserRole.free,
            ))
            db.commit()

        if not db.query(models.User).filter(models.User.email == "premium@latintunes.com").first():
            db.add(models.User(
                username="cliente_premium",
                email="premium@latintunes.com",
                hashed_password=hash_password("Premium@123"),
                role=models.UserRole.premium,
            ))
            db.commit()
            print("[seed] Test users created")

        # ── Albums & Songs ─────────────────────────────────────────────────────
        if db.query(models.Album).count() == 0:
            albums_data = [
                {
                    "title": "Sessions Vol. 1",
                    "year": 2024,
                    "cover_url": "",
                    "description": "Compilación de sesiones grabadas en LatinTunes Studio. Tracks de artistas emergentes de Medellín producidos íntegramente en el estudio.",
                    "is_premium": False,
                    "spotify_url": "",
                    "songs": [
                        {"title": "Ciudad de Luces", "track_number": 1, "duration": "3:42", "youtube_embed_id": None, "is_premium": False},
                        {"title": "Raíces ft. DJ Pulso", "track_number": 2, "duration": "4:10", "youtube_embed_id": None, "is_premium": False},
                    ]
                },
                {
                    "title": "Premium Cuts 2025",
                    "year": 2025,
                    "cover_url": "",
                    "description": "Selección exclusiva de producciones premium del catálogo LatinTunes. Mezcla y masterización de alta gama disponible solo para miembros premium.",
                    "is_premium": True,
                    "spotify_url": "",
                    "songs": [
                        {"title": "Madrugada Tropical", "track_number": 1, "duration": "3:55", "youtube_embed_id": None, "is_premium": True},
                        {"title": "Resonancia", "track_number": 2, "duration": "4:28", "youtube_embed_id": None, "is_premium": True},
                    ]
                },
            ]
            for album_info in albums_data:
                songs = album_info.pop("songs")
                album = models.Album(**album_info)
                db.add(album)
                db.flush()
                for s in songs:
                    db.add(models.Song(album_id=album.id, **s))
            db.commit()
            print("[seed] Albums and songs created")

        # ── Beats ──────────────────────────────────────────────────────────────
        if db.query(models.Beat).count() == 0:
            beats_data = [
                models.Beat(
                    title="Noche de Medellín",
                    description="Beat trap/latino con piano melódico y 808 profundos. Ideal para rap urbano o reguetón oscuro.",
                    category="Trap",
                    tags="trap,latino,piano,808,oscuro",
                    bpm=140,
                    musical_key="Am",
                    price=49.99,
                    is_available=True,
                    is_exclusive=False,
                ),
                models.Beat(
                    title="Cumbia Urbana",
                    description="Fusión de cumbia tradicional con producción moderna. Percusión en vivo, acordeón digital y bajos urbanos.",
                    category="Cumbia",
                    tags="cumbia,urbano,acordeón,percusión,colombia",
                    bpm=95,
                    musical_key="Dm",
                    price=39.99,
                    is_available=True,
                    is_exclusive=True,
                ),
            ]
            db.add_all(beats_data)
            db.commit()
            print("[seed] Beats created")

        # ── Services ───────────────────────────────────────────────────────────
        if db.query(models.Service).count() == 0:
            services_data = [
                models.Service(
                    name="Grabación Vocal Profesional",
                    description="Sesión de grabación en cabina tratada acústicamente con micrófono Neumann U87 y cadena de señal de alta gama.",
                    category=models.ServiceCategory.vocal_recording,
                    price_from=80.0,
                    duration_hours=2.0,
                    features=json.dumps(["Cabina acústica tratada", "Micrófono Neumann U87", "Ingeniero de grabación incluido", "Edición básica de vocales", "Entrega en 48h"]),
                    is_active=True,
                    sort_order=1,
                ),
                models.Service(
                    name="Mezcla y Masterización",
                    description="Mezcla profesional con procesamiento analógico y masterización para plataformas digitales (Spotify, Apple Music, etc.).",
                    category=models.ServiceCategory.mixing,
                    price_from=150.0,
                    duration_hours=4.0,
                    features=json.dumps(["Mezcla estéreo completa", "Masterización para streaming", "Hasta 2 revisiones", "Archivos WAV + MP3", "Entrega en 72h"]),
                    is_active=True,
                    sort_order=2,
                ),
            ]
            db.add_all(services_data)
            db.commit()
            print("[seed] Services created")

        # ── Packages ───────────────────────────────────────────────────────────
        if db.query(models.ServicePackage).count() == 0:
            packages_data = [
                models.ServicePackage(
                    name="Paquete Starter",
                    description="Ideal para artistas que están comenzando. Incluye grabación vocal y mezcla básica a un precio accesible.",
                    services_included=json.dumps(["Grabación Vocal (2h)", "Mezcla básica", "Masterización para streaming"]),
                    original_price=300.0,
                    discounted_price=270.0,
                    discount_pct=10,
                    is_active=True,
                    is_featured=False,
                ),
                models.ServicePackage(
                    name="Paquete Pro Studio",
                    description="El paquete más completo para producciones profesionales. Grabación, mezcla, masterización y diseño de portada.",
                    services_included=json.dumps(["Grabación Vocal (4h)", "Beat personalizado", "Mezcla profesional", "Masterización", "Diseño de portada"]),
                    original_price=600.0,
                    discounted_price=480.0,
                    discount_pct=20,
                    is_active=True,
                    is_featured=True,
                ),
            ]
            db.add_all(packages_data)
            db.commit()
            print("[seed] Packages created")

        # ── Equipment ──────────────────────────────────────────────────────────
        if db.query(models.Equipment).count() == 0:
            equipment_data = [
                models.Equipment(
                    name="Micrófono Neumann U87",
                    description="Micrófono de condensador de gran diafragma. Referente de la industria para grabación vocal y de instrumentos acústicos.",
                    category="Micrófonos",
                    brand="Neumann",
                    daily_rate=50.0,
                    weekly_rate=280.0,
                    deposit_amount=200.0,
                    is_available=True,
                    quantity_total=2,
                    quantity_available=2,
                ),
                models.Equipment(
                    name="Interface Universal Audio Apollo Twin X",
                    description="Interfaz de audio USB con procesamiento UAD integrado. 2 preamps UNISON, conversores de alta resolución 24-bit/192kHz.",
                    category="Interfaces",
                    brand="Universal Audio",
                    daily_rate=35.0,
                    weekly_rate=190.0,
                    deposit_amount=150.0,
                    is_available=True,
                    quantity_total=3,
                    quantity_available=3,
                ),
            ]
            db.add_all(equipment_data)
            db.commit()
            print("[seed] Equipment created")

        # ── Bookings ───────────────────────────────────────────────────────────
        if db.query(models.Booking).count() == 0:
            svc = db.query(models.Service).first()
            svc_id = svc.id if svc else None
            bookings_data = [
                models.Booking(
                    client_name="Carlos Rodríguez",
                    client_email="carlos.rodriguez@gmail.com",
                    client_phone="+57 310 555 0101",
                    service_id=svc_id,
                    service_type="Grabación Vocal Profesional",
                    booking_date=datetime.datetime(2025, 6, 15, 10, 0),
                    duration_hours=2.0,
                    status=models.BookingStatus.pending,
                    notes="Artista urbano, necesita cabina disponible de 10am a 12pm.",
                    total_price=160.0,
                ),
                models.Booking(
                    client_name="María López",
                    client_email="maria.lopez@hotmail.com",
                    client_phone="+57 315 555 0202",
                    service_id=svc_id,
                    service_type="Mezcla y Masterización",
                    booking_date=datetime.datetime(2025, 6, 18, 14, 0),
                    duration_hours=4.0,
                    status=models.BookingStatus.confirmed,
                    notes="Tiene 8 pistas grabadas, necesita mezcla completa y master para Spotify.",
                    total_price=150.0,
                    admin_notes="Confirmado. Pago recibido 50% por adelantado.",
                ),
            ]
            db.add_all(bookings_data)
            db.commit()
            print("[seed] Bookings created")

        # ── Licenses ───────────────────────────────────────────────────────────
        if db.query(models.License).count() == 0:
            beat = db.query(models.Beat).first()
            beat_id = beat.id if beat else None
            beat_title = beat.title if beat else "Beat sin título"
            licenses_data = [
                models.License(
                    license_number="LT-202506-DEMO0001",
                    beat_id=beat_id,
                    client_name="Juan Pérez",
                    client_email="juan.perez@gmail.com",
                    beat_title=beat_title,
                    license_type=models.LicenseType.basic,
                    status=models.LicenseStatus.active,
                    price_paid=49.99,
                    expiry_date=datetime.datetime(2026, 6, 1),
                    terms="Licencia básica no exclusiva. Uso permitido en plataformas digitales con crédito al productor. Máximo 10.000 streams.",
                    notes="Primera compra del cliente.",
                ),
                models.License(
                    license_number="LT-202506-DEMO0002",
                    beat_id=beat_id,
                    client_name="Andrea Silva",
                    client_email="andrea.silva@outlook.com",
                    beat_title=beat_title,
                    license_type=models.LicenseType.standard,
                    status=models.LicenseStatus.active,
                    price_paid=99.99,
                    expiry_date=datetime.datetime(2027, 6, 1),
                    terms="Licencia estándar no exclusiva. Uso ilimitado en plataformas digitales, radio y presentaciones en vivo.",
                    notes="Cliente recurrente — descuento del 10% aplicado.",
                ),
            ]
            db.add_all(licenses_data)
            db.commit()
            print("[seed] Licenses created")

        # ── Contact Messages ───────────────────────────────────────────────────
        if db.query(models.ContactMessage).count() == 0:
            messages_data = [
                models.ContactMessage(
                    name="Diego Martínez",
                    email="diego.martinez@gmail.com",
                    subject="Información sobre grabación",
                    message="Hola, soy artista independiente y quiero saber más sobre sus servicios de grabación vocal. ¿Tienen disponibilidad para la próxima semana? ¿Cuál es el precio por hora?",
                    is_read=False,
                ),
                models.ContactMessage(
                    name="Laura Gómez",
                    email="laura.gomez@hotmail.com",
                    subject="Cotización paquete completo",
                    message="Buenos días. Estoy interesada en el paquete Pro Studio para grabar mi primer EP de 5 canciones. ¿Podrían enviarme una cotización detallada con tiempos de entrega?",
                    is_read=True,
                ),
            ]
            db.add_all(messages_data)
            db.commit()
            print("[seed] Contact messages created")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_initial_data()
    yield


app = FastAPI(
    title="LatinTunes API",
    description="Backend for LatinTunes — Productora Musical",
    version="2.0.0",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(albums.router)
app.include_router(admin.router)
app.include_router(contact.router)
app.include_router(beats.router)
app.include_router(services.router)
app.include_router(equipment.router)
app.include_router(bookings.router)
app.include_router(licenses.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "LatinTunes API"}
