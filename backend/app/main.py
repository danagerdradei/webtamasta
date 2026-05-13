from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import engine, Base
from .config import settings
from .routers import auth, albums, admin, contact, beats, services, equipment, bookings, licenses
from . import models


def seed_initial_data():
    from sqlalchemy.orm import Session
    from .auth import hash_password

    with Session(engine) as db:
        # Admin user
        if not db.query(models.User).filter(models.User.email == settings.ADMIN_EMAIL).first():
            db.add(models.User(
                username="latintunes_admin",
                email=settings.ADMIN_EMAIL,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                role=models.UserRole.admin,
            ))
            db.commit()
            print(f"[seed] Admin created: {settings.ADMIN_EMAIL}")

        # Visitor test user
        if not db.query(models.User).filter(models.User.email == "visitante@latintunes.com").first():
            db.add(models.User(
                username="visitante",
                email="visitante@latintunes.com",
                hashed_password=hash_password("Visitante@123"),
                role=models.UserRole.free,
            ))
            db.commit()
            print("[seed] Visitor test user created: visitante@latintunes.com")

        # Premium test user
        if not db.query(models.User).filter(models.User.email == "premium@latintunes.com").first():
            db.add(models.User(
                username="cliente_premium",
                email="premium@latintunes.com",
                hashed_password=hash_password("Premium@123"),
                role=models.UserRole.premium,
            ))
            db.commit()
            print("[seed] Premium test user created: premium@latintunes.com")

        if db.query(models.Album).count() == 0:
            albums_data = [
                {
                    "title": "Rapresent",
                    "year": 2021,
                    "cover_url": "",
                    "description": "Primer álbum de Atamasta. Boom bap puro representando el Rap Latino desde Colombia y Ecuador. Producido íntegramente por Golden Fingaz.",
                    "is_premium": False,
                    "spotify_url": "https://open.spotify.com/artist/0pKlzt6G9f8KCTVXr8SUyM",
                    "songs": [
                        {"title": "Rapresent ft. MNZ", "track_number": 1, "duration": "3:59", "youtube_embed_id": None, "is_premium": False},
                        {"title": "Nordafackaz #1 (North Down Clica)", "track_number": 2, "duration": "2:30", "youtube_embed_id": None, "is_premium": False},
                        {"title": "Boombapkistan", "track_number": 3, "duration": "3:06", "youtube_embed_id": "hbHfP9hn6js", "is_premium": False},
                        {"title": "Cypher II - Lo Bueno Ya Viene", "track_number": 4, "duration": "3:45", "youtube_embed_id": "qIs4iNg2wVA", "is_premium": False},
                    ]
                },
                {
                    "title": "Golden Era",
                    "year": 2023,
                    "cover_url": "",
                    "description": "El álbum más completo de Atamasta. Diez canciones de boom bap puro inspiradas en el Hip Hop de los 90s. Producción 100% de Golden Fingaz.",
                    "is_premium": True,
                    "spotify_url": "https://open.spotify.com/artist/0pKlzt6G9f8KCTVXr8SUyM",
                    "songs": [
                        {"title": "Perros de Raza", "track_number": 1, "duration": "2:39", "youtube_embed_id": None, "is_premium": True},
                        {"title": "Molotov Rocket", "track_number": 2, "duration": "3:14", "youtube_embed_id": "HjHMqBeX9qI", "is_premium": True},
                        {"title": "Rap Sinatra", "track_number": 3, "duration": "5:46", "youtube_embed_id": None, "is_premium": True},
                        {"title": "Lingotes Andinos", "track_number": 4, "duration": "3:28", "youtube_embed_id": None, "is_premium": True},
                        {"title": "Homura Damma ft Da Flava", "track_number": 5, "duration": "4:00", "youtube_embed_id": None, "is_premium": True},
                        {"title": "Polo Norte ft Ermitaño Mental", "track_number": 6, "duration": "2:58", "youtube_embed_id": None, "is_premium": True},
                        {"title": "Al Otro Lado Del Edén", "track_number": 7, "duration": "3:16", "youtube_embed_id": None, "is_premium": True},
                        {"title": "En Peligro De Extinción", "track_number": 8, "duration": "2:56", "youtube_embed_id": None, "is_premium": True},
                        {"title": "Smocka Funk", "track_number": 9, "duration": "3:34", "youtube_embed_id": None, "is_premium": True},
                        {"title": "From Da Block", "track_number": 10, "duration": "3:01", "youtube_embed_id": None, "is_premium": True},
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
