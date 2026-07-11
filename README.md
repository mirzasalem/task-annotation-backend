# Task & Annotation — Backend

Django API used by the task board and image annotation frontend.

**Author:** Mirza Salem  
GitHub: [mirzasalem](https://github.com/mirzasalem) · Email: mirza.salem2016@gmail.com

Frontend repo: [task-annotation-frontend](https://github.com/mirzasalem/task-annotation-frontend)

---

## Demo

| | |
|--|--|
| API URL | https://mirzasalem.pythonanywhere.com |
| Frontend | https://task-annotation-frontend.vercel.app |
| Login | https://task-annotation-frontend.vercel.app/login |
| Frontend repo | https://github.com/mirzasalem/task-annotation-frontend |

Demo user (script: `create_demo_user.py`):

- Email: `demo@vai-radiology.com`
- Password: `Demo@1234`

---

## Stack

Python 3.12, Django, Django REST Framework, SQLite (ORM), Pillow, django-cors-headers, gunicorn

**Python version used:** `3.12.3`

---

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # optional
python manage.py migrate
python create_demo_user.py
python manage.py runserver 0.0.0.0:8000
```

API: http://localhost:8000

Useful env vars: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS` (see `.env.example`).

---

## What it exposes

Auth: `/api/auth/csrf/`, `login/`, `logout/`, `me/`

Tasks: CRUD on `/api/tasks/` (filter with `?scheduled_date=YYYY-MM-DD`), plus `POST /api/tasks/reorder/`

Annotations: `/api/annotations/images/` (list/upload/delete), `POST /api/annotations/polygons/bulk_save/`

`bulk_save` body looks like:

```json
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

It clears old polygons for that image, then inserts the new ones.

---

## Models

- `Task` — title, priority, due_date, scheduled_date, tags, status, order, user
- `AnnotatedImage` — uploaded file + user
- `PolygonAnnotation` — points (JSON), color, label, FK to image

---

## Apps

`accounts`, `tasks`, `annotations`, plus `config` for settings/urls.

---

## Problems I hit (and fixes)

**CSRF + CORS with a separate frontend origin**  
Browser blocked cookie requests until I enabled credentials CORS and sent `X-CSRFToken` from the frontend. In DEBUG I also relax CSRF on `/api/` so local port mismatches don’t block development.

**Storing polygons**  
I used a JSON field for the point list instead of a Point table. Frontend sends the full list; `bulk_save` replaces rows for that image so DB state matches the canvas.

**DnD order**  
One reorder endpoint updates many tasks at once after a drop, instead of one PATCH per card.

---

## Deploy

Render / PythonAnywhere both work. Example start command:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Set `DEBUG=False`, a real `SECRET_KEY`, and CORS/CSRF origins to your frontend domain. Run migrate + `create_demo_user.py` on deploy. Uploaded images need disk that survives restarts (or accept re-upload for the demo).

`Procfile` and `render.yaml` are included.

---

## Author

Mirza Salem — [github.com/mirzasalem](https://github.com/mirzasalem) — mirza.salem2016@gmail.com
