# Task & Annotation — Backend

Django REST API for **authentication**, **Kanban tasks**, and **image polygon annotations**.

**Author:** Mirza Salem ([mirzasalem](https://github.com/mirzasalem))  
**Email:** mirza.salem2016@gmail.com

**Companion frontend repo:** `task-annotation-frontend` (Next.js / TypeScript)

---

## Live demo

| Resource | URL |
|----------|-----|
| API (hosted) | _add Render / PythonAnywhere URL_ |
| Frontend (hosted) | _add Vercel URL_ |
| Frontend GitHub | _add frontend repo URL_ |

### Demo login

| Email | Password |
|-------|----------|
| `demo@vai-radiology.com` | `Demo@1234` |

Create/update the demo user anytime:

```bash
python create_demo_user.py
```

---

## Tech stack

- **Python 3.12**
- **Django 6.x**
- **Django REST Framework**
- **django-cors-headers**
- **SQLite** (Django ORM) — Postgres-ready via settings
- **Pillow** — image uploads
- **gunicorn** — production server

### Versions

| Tool | Version (tested) |
|------|------------------|
| Python | 3.12.3 |

---

## Features

- Session-based login (email + password) with CSRF support for SPA
- Task CRUD filtered by `scheduled_date`
- Bulk reorder after drag-and-drop (`status` + `order`)
- Multipart image upload
- Polygon `bulk_save` (replace-all for an image) for persistence

---

## Setup & run

### Prerequisites

- Python 3.12+
- pip

### Install

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # optional for local
python manage.py migrate
python create_demo_user.py
python run_dev.py                 # listens on 0.0.0.0:8000
# or: python manage.py runserver 0.0.0.0:8000
```

API base: **http://localhost:8000**

### Environment (`.env` / host env vars)

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django secret (required in production) |
| `DEBUG` | `True` locally; `False` in production |
| `ALLOWED_HOSTS` | Comma-separated hosts |
| `CORS_ALLOWED_ORIGINS` | Frontend origins (e.g. `http://localhost:3000`) |
| `CSRF_TRUSTED_ORIGINS` | Same frontend origins with scheme |

See `.env.example` for a local starting point.

---

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/csrf/` | CSRF token |
| POST | `/api/auth/login/` | Login (email + password) |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Current user |
| GET | `/api/tasks/?scheduled_date=YYYY-MM-DD` | List tasks for a date |
| POST | `/api/tasks/` | Create task |
| PATCH | `/api/tasks/:id/` | Update task |
| DELETE | `/api/tasks/:id/` | Delete task |
| POST | `/api/tasks/reorder/` | Bulk update status/order after DnD |
| GET | `/api/annotations/images/` | List images (+ nested polygons) |
| POST | `/api/annotations/images/` | Upload image (multipart) |
| DELETE | `/api/annotations/images/:id/` | Delete image |
| POST | `/api/annotations/polygons/bulk_save/` | Replace all polygons for an image |

### Example: save polygons

```json
POST /api/annotations/polygons/bulk_save/
{
  "image_id": 3,
  "polygons": [
    {
      "points": [{"x": 120, "y": 80}, {"x": 200, "y": 90}, {"x": 180, "y": 160}],
      "label": "",
      "color": "#f7941d"
    }
  ]
}
```

Backend deletes existing polygons for that image, then creates new rows (ORM + `JSONField` for points).

---

## Models

| Model | Main fields |
|-------|-------------|
| **Task** | user, title, priority, due_date, scheduled_date, tags (JSON), status, order |
| **AnnotatedImage** | user, image (ImageField), name |
| **PolygonAnnotation** | image (FK), points (JSON), label, color |

All queries use **Django ORM** (SQLite by default).

---

## Project structure

```
├── accounts/          # auth views (csrf, login, logout, me)
├── tasks/             # Task model, serializers, viewset + reorder
├── annotations/       # AnnotatedImage, PolygonAnnotation, bulk_save
├── config/            # settings, urls, middleware, wsgi
├── create_demo_user.py
├── manage.py
├── run_dev.py
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```

---

## Challenges & how I overcame them

**Session auth + CORS with a Next.js SPA**  
Mutating requests need CSRF. The frontend fetches a CSRF token and sends it with cookies (`CORS_ALLOW_CREDENTIALS`). Trusted origins must include the frontend URL (localhost and production).

**Image annotation coordinates**  
Canvas clicks are scaled to the image’s natural dimensions so stored `{x,y}` points stay correct when the image is displayed smaller than full size.

**Drag-and-drop persistence**  
A dedicated `reorder` action updates many tasks’ `status` and `order` in one request after a drop, without a full board rewrite on the client.

**Polygon persistence**  
`bulk_save` uses a replace-all strategy so the database always matches the current canvas state after Finish or Remove.

---

## Deploy (Render / PythonAnywhere)

1. Connect this GitHub repo as a web service.
2. Build: `pip install -r requirements.txt && python manage.py migrate && python create_demo_user.py`
3. Start: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` (see `Procfile` / `render.yaml`)
4. Set production env: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`
5. Run `collectstatic` if you serve admin/static; configure **persistent media** for uploads

---

## Author

**Mirza Salem**  
GitHub: [mirzasalem](https://github.com/mirzasalem)  
Email: mirza.salem2016@gmail.com

---

## License

Built as a fullstack engineering assignment. © Mirza Salem.
