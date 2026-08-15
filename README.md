# 📚 Book Analytics API

A production-style analytics REST API built with **FastAPI**, demonstrating clean architecture, JWT-style authentication, CSV export, containerisation, and CI/CD deployment to Kubernetes.

> Built as a portfolio project to showcase backend engineering skills.

---

## 🏗️ Architecture

```
Request → API Key Auth → Endpoint → Service → Repository → SQLite/DB
                                                         ↓
                                             pandas DataFrame
                                                         ↓
                                       JSON response OR CSV StreamingResponse
```

### Layers

| Layer | Responsibility |
|---|---|
| `endpoints/` | HTTP routing, query param validation |
| `services/` | Business logic, pagination, CSV export |
| `repositories/` | Parameterised SQL only — no business logic |
| `schemas/` | Pydantic models — request/response validation |
| `utils/csv_exporter.py` | Reusable CSV streaming utility |
| `core/security.py` | API key auth (drop-in replacement for JWT) |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/book-analytics-api.git
cd book-analytics-api

# Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/dev.txt

# Seed demo data
python scripts/seed.py

# Run
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000/api/docs** — use `X-API-Key: dev-api-key-change-in-production`

---

## 📡 Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/actuator/health` | Health check (no auth) |
| `GET` | `/api/v1/books` | Paginated book catalogue with filters |
| `GET` | `/api/v1/books/export` | Download full catalogue as CSV |
| `GET` | `/api/v1/sales-summary` | Revenue analytics by genre |
| `GET` | `/api/v1/sales-summary/export` | Download sales summary as CSV |
| `GET` | `/api/v1/top-borrowers` | Members with most borrows |
| `GET` | `/api/v1/top-borrowers/export` | Download top borrowers as CSV |

All endpoints except `/actuator/health` require: `X-API-Key: <your-key>`

---

## 🐳 Docker

```bash
docker compose up --build
# API available at http://localhost:8000/api/docs
```

---

## ✅ Tests

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## 🔧 Key Skills Demonstrated

- **FastAPI** — layered architecture, dependency injection, Pydantic validation
- **SQLAlchemy + pandas** — parameterised SQL, DataFrame-based data pipeline
- **CSV export** — reusable streaming utility (zero temp files)
- **Security** — API key auth with clean swap path to JWT
- **Docker** — multi-stage build, non-root user, Gunicorn + Uvicorn
- **Kubernetes** — Helm chart with forced rollout on every deploy
- **CI/CD** — GitHub Actions: test → build → push → helm upgrade
- **Testing** — pytest