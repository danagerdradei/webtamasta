# Atamasta Official Website

Website completo para el artista de rap **Atamasta** (AKA "Golden Fingaz").

## Tecnologías

| Capa | Stack |
|------|-------|
| Frontend | HTML5 + CSS3 + Vanilla JS (sin frameworks) |
| Backend | Python 3.12 + FastAPI + SQLAlchemy |
| Base de datos | PostgreSQL 16 |
| Auth | JWT (python-jose + bcrypt) |
| Deploy | Docker + Docker Compose |

## Estructura

```
Webtamasta/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app + lifespan seed
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── auth.py          # JWT + password hashing
│   │   ├── database.py      # DB session
│   │   ├── config.py        # Settings (.env)
│   │   └── routers/
│   │       ├── auth.py      # /api/auth/*
│   │       ├── albums.py    # /api/albums/*
│   │       ├── admin.py     # /api/admin/*
│   │       └── contact.py   # /api/contact
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html           # Landing page principal
│   ├── css/main.css         # Estilos globales + animaciones
│   ├── js/
│   │   ├── api.js           # Cliente API centralizado
│   │   ├── utils.js         # Utilidades compartidas
│   │   └── main.js          # Lógica del landing + player
│   └── pages/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       └── admin.html       # Panel de administración
└── docker-compose.yml
```

## Inicio rápido

### Opción A — Docker (recomendado)
```bash
docker-compose up -d
```

### Opción B — Local (Windows)
```
start-backend.bat
```
Luego abre `frontend/index.html` con Live Server (VS Code) o cualquier servidor estático.

### Requisitos locales
- Python 3.11+
- PostgreSQL 14+ corriendo localmente
- Editar `backend/.env` con tus credenciales de DB

## Credenciales por defecto

| Campo | Valor |
|-------|-------|
| Admin email | `admin@atamasta.com` |
| Admin password | `Admin@12345` |

## API Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/register` | Registrar usuario |
| POST | `/api/auth/login` | Login → JWT token |
| GET | `/api/auth/me` | Perfil del usuario actual |
| GET | `/api/albums` | Listar álbumes |
| GET | `/api/albums/{id}` | Detalle de álbum |
| PATCH | `/api/admin/users/{id}` | Banear / cambiar rol |
| GET | `/api/admin/stats` | Estadísticas del panel |
| POST | `/api/contact` | Enviar mensaje de contacto |

Documentación interactiva: **http://localhost:8000/docs**

## Roles de usuario

| Rol | Acceso |
|-----|--------|
| `free` | Álbumes gratuitos |
| `premium` | Todo el contenido |
| `admin` | Panel de administración + todo |

## Features implementados

- Landing page animada con partículas y secciones: Hero, About, Discografía, Player, Videos, Contacto
- Reproductor de música con lista de pistas, progreso, anterior/siguiente
- Modal de videos YouTube embebidos
- Sistema de autenticación completo (registro, login, JWT)
- Panel de administración: estadísticas, gestión de usuarios, baneos, álbumes, mensajes
- Roles y permisos (free, premium, admin)
- Formulario de contacto/marketing guardado en BD
- Diseño responsivo (móvil + escritorio)
- Tema oscuro con paleta dorada/roja (branding Atamasta)
