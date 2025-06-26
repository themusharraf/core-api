# 🧠 Coffee shop API — FastAPI Microservice with PostgreSQL, Redis, Celery

This project is a scalable FastAPI backend application using:

- FastAPI – Web framework
- SQLAlchemy – ORM for database interaction
- Celery & Celery Beat – For background task processing and scheduling
- Redis – Used as a Celery broker
- PostgreSQL – Main database
- Docker & Docker Compose – For containerization
---

## 🚀 Getting Started

### 📦 1. Clone and Setup

```bash
https://github.com/themusharraf/core-api.git
cd core_api
cp .env_dist .env
```

## 🐳 2. Run with Docker Compose

```bash
docker-compose up -d --build
```

## ⚙️ Architecture

```
core_api/
│
├── core/               # App-level core settings and utilities
│   ├── config.py       # Environment and settings management
│   ├── db.py           # DB session setup
│   ├── enum.py         # Enums used throughout the project
│   ├── exceptions.py   # Custom exception classes
│   └── logger.py       # Logging configuration
│
├── dependencies/       # FastAPI dependencies (auth, db, etc.)
│
├── models/             # SQLAlchemy models
│
├── schemas/            # Pydantic schemas for request/response
│
├── services/           # Business logic layer
│
├── routers/            # FastAPI routers (endpoints)
│
├── tasks/              # Celery background jobs (cleanup, emails, etc.)
│
├── utils/              # Reusable helpers email sending
│
├── logs/               # Application logs
│
├── main.py             # Entry point for FastAPI app
├── celery_worker.py    # Celery app instance
├── Dockerfile          # Build image for FastAPI
├── docker-compose.yml  # Define services
└── requirements.txt    # Dependencies

```