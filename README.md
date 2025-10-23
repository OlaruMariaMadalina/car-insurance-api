# Car Insurance API

A FastAPI-based backend for managing car insurance, owners, policies, claims, and related operations.

## Features

- CRUD operations for Owners, Cars, Insurance Policies, and Claims
- Policy expiry background job (APScheduler)
- Health check endpoint
- Structured logging with structlog
- Database migrations with Alembic
- Pydantic validation and OpenAPI docs
- **Dockerized PostgreSQL database for development**

## Project Structure

```
app/
  config.py            # Application settings
  main.py              # FastAPI app entrypoint
  scheduler.py         # Background job scheduler
  db/                  # Database setup and migrations
  jobs/                # Background job logic
  logging/             # Logging configuration
  models/              # SQLAlchemy ORM models
  routers/             # FastAPI routers (API endpoints)
  schemas/             # Pydantic schemas
  scripts/             # Utility scripts (e.g., seed_db.py)
  utils/               # Utility modules (e.g., db dependencies)
docker-compose.yaml    # Docker Compose file for PostgreSQL
```

## Setup

### 1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### 2. **Configure environment**
   - Copy `.env.example` to `.env` and adjust settings as needed (DB URL, log level, etc).
   - Example for PostgreSQL:
     ```
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=postgres
     POSTGRES_DB=car_insurance
     DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/car_insurance
     ```

### 3. **Start PostgreSQL with Docker**
   ```bash
   docker-compose up -d
   ```
   This will start a PostgreSQL 16 database in a container, exposed on port 5432.

### 4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

### 5. **Seed the database (optional)**
   ```bash
   python app/scripts/seed_db.py
   ```

### 6. **Start the API server**
   ```bash
   uvicorn app.main:app --reload
   ```

### 7. **Access API docs**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## Docker & PostgreSQL

- The project includes a `docker-compose.yaml` for running a PostgreSQL database locally.
- Data is persisted in a Docker volume (`carins_pgdata`).
- The database is automatically health-checked and restarted if needed.

## Background Jobs

- Policy expiry scan runs periodically (interval configurable in `config.py`).
- Scheduler starts automatically with the app.

## Development

- Routers are modular (see `app/routers/`)
- Models and schemas are separated for clarity
- Logging is structured and configurable

## Migrations

- Alembic migration scripts are in `app/db/migrations/versions/`
- To create a new migration:
  ```bash
  alembic revision --autogenerate -m "your message"
  alembic upgrade head
  ```