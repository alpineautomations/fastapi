# Python API Development — Notes

**Source:** freeCodeCamp.org — "Python API Development - Comprehensive Course for Beginners" (~19 hours). Course by Sanjeev Thiyagarajan. Stack: **FastAPI**, PostgreSQL, SQLAlchemy, Alembic, pytest, Docker, CI/CD.

> These notes follow the video's order. Commands are written in correct shell form. Points where the video is loose or leaves a gap are flagged **⚠️ Note**.

---

## 1. Setup & environment

- Python version, virtual environment (`python -m venv venv`), activating it.
- Installing FastAPI + Uvicorn.
- Project structure.

---

## 2. FastAPI basics

- First endpoint, running with `uvicorn main:app --reload`.
- Path operations, HTTP methods, `/docs` (Swagger) and `/redoc`.

---

## 3. Request & response

- Pydantic models / schemas.
- Request body, path & query parameters.
- Response models, status codes.

---

## 4. Database

- Raw SQL with `psycopg2` vs ORM.
- SQLAlchemy models, sessions, `get_db` dependency.
- CRUD operations.

---

## 5. Auth

- Password hashing (`passlib` / bcrypt).
- JWT tokens, OAuth2 password flow.
- Protecting routes with dependencies.

---

## 6. Relationships & queries

- Foreign keys, table relationships.
- Joins, filtering, pagination, search.
- Votes / likes feature.

---

## 7. Migrations — Alembic

- Init, autogenerate, upgrade / downgrade.

---

## 8. Config & environment variables

- Pydantic `BaseSettings`, `.env` file.

---

## 9. CORS

---

## 10. Testing — pytest

- Fixtures, test database, testing auth, parametrize.

---

## 11. Deployment

- Docker & docker-compose.
- Deploying (Ubuntu VPS / Heroku).
- Gunicorn + Uvicorn workers, systemd, NGINX.

---

## 12. CI/CD

- GitHub Actions pipeline: test → build → deploy.
