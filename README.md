# LatinTunes — Studio Website

Plataforma web completa para **LatinTunes**, estudio de producción musical profesional ubicado en Medellín.

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Frontend | HTML5 + CSS3 + Vanilla JS (sin frameworks) |
| Backend | Python 3.12 + FastAPI + SQLAlchemy ORM |
| Base de datos | PostgreSQL 16 |
| Autenticación | JWT (python-jose + bcrypt) |
| Contenedores | Docker + Docker Compose |

---

## Estructura del proyecto

```
Webtamasta/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + lifespan (seed admin)
│   │   ├── models.py          # SQLAlchemy models (ORM)
│   │   ├── schemas.py         # Pydantic v2 schemas
│   │   ├── auth.py            # JWT + password hashing
│   │   ├── database.py        # Sesión de base de datos
│   │   ├── config.py          # Settings desde .env
│   │   └── routers/
│   │       ├── auth.py        # /api/auth/*
│   │       ├── albums.py      # /api/albums/*
│   │       ├── beats.py       # /api/beats/*
│   │       ├── services.py    # /api/services/* + /api/services/packages/*
│   │       ├── equipment.py   # /api/equipment/*
│   │       ├── bookings.py    # /api/bookings/*
│   │       ├── licenses.py    # /api/licenses/*
│   │       ├── contact.py     # /api/contact
│   │       └── admin.py       # /api/admin/*
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html             # Landing page principal
│   ├── img/
│   │   ├── LatinTunes.jpeg    # Logo circular (color)
│   │   ├── LatinTunesWhite.jpeg # Logo circular (blanco, usado en hero vinyl)
│   │   └── banner.jpg         # Imagen de fondo del hero
│   ├── css/
│   │   ├── main.css           # Estilos globales, navbar, hero, utilidades
│   │   └── pages.css          # Estilos específicos de páginas internas
│   ├── js/
│   │   ├── api.js             # Cliente API centralizado (todos los endpoints)
│   │   ├── navbar.js          # Inyector de navbar compartida
│   │   ├── utils.js           # initNavbar, updateNavAuth, initScrollReveal
│   │   └── main.js            # Lógica del landing
│   └── pages/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html     # Perfil del usuario autenticado
│       ├── admin.html         # Panel de administración (10 tabs)
│       ├── services.html      # Catálogo de servicios del estudio
│       ├── booking.html       # Formulario de reserva de sesiones
│       ├── beats.html         # Tienda de beats (con reproductor y filtros)
│       ├── packages.html      # Planes y paquetes del estudio
│       ├── equipment.html     # Inventario de equipos disponibles
│       ├── about.html         # Página institucional "Nosotros"
│       ├── contact.html       # Formulario de contacto
│       ├── music.html         # Catálogo de música / álbumes
│       ├── discography.html   # Discografía
│       └── videos.html        # Galería de videos
├── docker-compose.yml
└── start-backend.bat          # Arranque local (Windows)
```

---

## Inicio rápido

### Opción A — Docker (recomendado)

```bash
docker compose up -d
```

Esto levanta dos servicios:
- `latintunes_db` — PostgreSQL 16 en puerto `5432`
- `latintunes_backend` — FastAPI en puerto `8000`

El admin por defecto se crea automáticamente al arrancar.

### Opción B — Local (Windows)

```bat
start-backend.bat
```

Luego abre `frontend/index.html` con Live Server (VS Code) o cualquier servidor estático.

**Requisitos locales:**
- Python 3.11+
- PostgreSQL 14+ corriendo localmente
- Configurar `backend/.env` con las credenciales de la BD

### Rebuilding el backend (tras cambios en modelos)

```bash
docker compose build backend && docker compose up -d backend
```

---

## Credenciales por defecto

| Campo | Valor |
|-------|-------|
| Admin email | `admin@latintunes.com` |
| Admin password | `Admin@12345` |

---

## API — Endpoints

### Autenticación

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/register` | Registrar nuevo usuario |
| POST | `/api/auth/login` | Login → retorna JWT token |
| GET | `/api/auth/me` | Perfil del usuario autenticado |

### Beats

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/beats` | Listar beats (filtros: genre, mood, bpm, search) |
| GET | `/api/beats/{id}` | Detalle de beat |
| GET | `/api/beats/categories` | Géneros disponibles |
| POST | `/api/beats/{id}/play` | Registrar reproducción |
| POST | `/api/beats` | Crear beat (admin) |
| PUT | `/api/beats/{id}` | Editar beat (admin) |
| DELETE | `/api/beats/{id}` | Eliminar beat (admin) |

### Servicios y Paquetes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/services` | Listar servicios activos |
| GET | `/api/services/categories` | Categorías de servicio |
| POST | `/api/services` | Crear servicio (admin) |
| PUT | `/api/services/{id}` | Editar servicio (admin) |
| DELETE | `/api/services/{id}` | Eliminar servicio (admin) |
| GET | `/api/services/packages/all` | Listar paquetes |
| POST | `/api/services/packages` | Crear paquete (admin) |
| PUT | `/api/services/packages/{id}` | Editar paquete (admin) |
| DELETE | `/api/services/packages/{id}` | Eliminar paquete (admin) |

### Equipos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/equipment` | Listar equipos (filtro: available_only) |
| GET | `/api/equipment/categories` | Categorías de equipos |
| POST | `/api/equipment` | Crear equipo (admin) |
| PUT | `/api/equipment/{id}` | Editar equipo (admin) |
| DELETE | `/api/equipment/{id}` | Eliminar equipo (admin) |

### Reservas

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/bookings` | Crear reserva (usuario autenticado) |
| GET | `/api/bookings` | Listar reservas (admin, filtro por status) |
| PATCH | `/api/bookings/{id}` | Actualizar estado/precio (admin) |
| DELETE | `/api/bookings/{id}` | Eliminar reserva (admin) |

### Licencias

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/licenses/verify/{number}` | Verificar licencia por número (público) |
| GET | `/api/licenses` | Listar licencias (admin) |
| GET | `/api/licenses/{id}` | Detalle de licencia (admin) |
| POST | `/api/licenses` | Emitir licencia (admin) |
| PATCH | `/api/licenses/{id}` | Actualizar licencia (admin) |
| DELETE | `/api/licenses/{id}` | Eliminar licencia (admin) |

Formato de número de licencia: `LT-YYYYMM-XXXXXXXX`

### Contacto y Admin

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/contact` | Enviar mensaje de contacto |
| GET | `/api/admin/users` | Listar usuarios (admin) |
| PATCH | `/api/admin/users/{id}` | Banear / cambiar rol (admin) |
| DELETE | `/api/admin/users/{id}` | Eliminar usuario (admin) |
| GET | `/api/admin/stats` | Estadísticas generales (admin) |
| GET | `/api/admin/messages` | Listar mensajes de contacto (admin) |
| PATCH | `/api/admin/messages/{id}/read` | Marcar mensaje como leído (admin) |

Documentación interactiva: **http://localhost:8000/docs**

---

## Roles de usuario

| Rol | Acceso |
|-----|--------|
| `free` | Contenido público, beats gratuitos, formularios |
| `premium` | Todo el contenido premium y beats exclusivos |
| `admin` | Panel de administración completo |

---

## Panel de administración (`/pages/admin.html`)

Sidebar con 10 tabs organizados en 4 secciones:

| Sección | Tabs |
|---------|------|
| Principal | Dashboard (stats + actividad reciente) |
| Operaciones | Reservas, Servicios, Paquetes, Equipos, Licencias |
| Contenido | Beats, Música (álbumes) |
| Sistema | Usuarios, Mensajes |

Funcionalidades por tab:
- **Dashboard** — estadísticas de usuarios, reservas, equipos, licencias activas y mensajes no leídos
- **Reservas** — gestión completa con cambio de estado, precio y notas; badge de pendientes
- **Servicios** — CRUD con categorías, precio base, duración, features en lista
- **Paquetes** — CRUD con servicios incluidos y descuento
- **Equipos** — inventario con tarifas diarias/semanales, disponibilidad y depósito
- **Licencias** — emisión, verificación pública por número, revocar/activar, eliminar
- **Beats** — catálogo con precio, género, BPM, estado (free/premium)
- **Música** — álbumes y canciones
- **Usuarios** — listar, cambiar rol (free/premium/admin), banear/desbanear, eliminar
- **Mensajes** — bandeja de contacto con marcar como leído; badge de no leídos

---

## Diseño y branding

- **Tema:** oscuro (`#060809`) con acento plateado (`#a8b8c8`) — variable CSS `--gold`
- **Tipografías:** Rajdhani (display) + Inter (cuerpo) — Google Fonts
- **Hero:** vinyl animado con logo LatinTunes, stats del estudio, scroll hint
- **Componentes:** cards con hover lift, modales, toasts de notificación, scroll reveal
- **Responsive:** navbar hamburger en móvil, grids adaptativos, breakpoints en 768px / 480px

---

## Variables de entorno (`backend/.env`)

```env
DATABASE_URL=postgresql://latintunes:latintunes@db:5432/latintunes
SECRET_KEY=cambia_esto_en_produccion
ADMIN_EMAIL=admin@latintunes.com
ADMIN_PASSWORD=Admin@12345
```
