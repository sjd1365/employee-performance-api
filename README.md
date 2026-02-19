# Employee Performance API

FastAPI backend for employee performance analytics using Neon PostgreSQL.

## Endpoints
- GET `/health`
- GET `/reports/top-employees`
- GET `/reports/dept-trend`
- GET `/employee/{employee_code}/efficiency`

## Environment variable
Set this in your environment (locally or on deploy platform):
- `DATABASE_URL` = your Neon Postgres connection string (with sslmode=require)

## Run locally
```bash
pip install -r requirements.txt
export DATABASE_URL="YOUR_NEON_URL"
uvicorn main:app --reload

