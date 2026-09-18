# CaseNext

**Know what happens next.**

CaseNext helps university students facing an academic misconduct / academic
integrity case understand where they are in their school's process, what
may happen next, what to prepare, and what other students have experienced
in similar cases.

Every university has its own terminology, offices, and procedures.
CaseNext never forces a generic workflow onto a school — each school's
actual terms and steps are stored and shown as-is. A lightweight shared
"category" field exists only for cross-school search/filtering.

This repo is being built incrementally. See below for what's done so far.

## Status: Phase 1 — Backend foundation

Done in this phase:
- Flask app (application factory pattern) connected to PostgreSQL via
  Flask-SQLAlchemy
- Database schema for all 11 core entities (schools, offices, terminology,
  workflows, workflow steps, allegation types, resources, cases, case
  details, case events, case outcomes)
- Flask-Migrate set up with an initial migration
- Seed script with two sample schools (Arizona State University and
  University of Illinois Urbana-Champaign) that intentionally use
  different terminology and workflow steps, to prove the schema doesn't
  assume a universal process

Not built yet (later phases): REST API endpoints, React frontend, AI
features.

## Project structure

```
backend/
  app/
    __init__.py        # Flask app factory
    config.py           # Configuration (reads DATABASE_URL etc. from .env)
    extensions.py        # Shared db/migrate instances
    models/              # One file per database table
    routes/               # REST API endpoints (Phase 2)
  migrations/            # Flask-Migrate / Alembic migration history
  seed.py                # Populates sample schools/cases for local dev
  run.py                 # App entry point
  requirements.txt
  .env.example           # Copy to .env and fill in DB credentials
```

## Running the backend locally

Requirements: Python 3.11+, PostgreSQL running locally.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env if your Postgres user/password/db name differ

# Create the database (adjust user/db name to match your .env)
createdb casenext_dev   # or: psql -c "CREATE DATABASE casenext_dev;"

# Apply the database schema
export FLASK_APP=run.py
flask db upgrade

# Load sample data (2 schools with distinct workflows/terminology)
python seed.py

# Start the API
flask run
```

Visit `http://127.0.0.1:5000/api/health` — it should return `{"status": "ok"}`.

## What to test after Phase 1

1. `flask db upgrade` runs without errors and creates 11 tables plus
   `alembic_version` (check with `psql -d casenext_dev -c "\dt"`).
2. `python seed.py` runs without errors and prints the two seeded school
   names.
3. Spot-check the data, e.g.:
   ```sql
   SELECT s.name, w.name, ws."order", ws.name, ws.actor
   FROM schools s
   JOIN workflows w ON w.school_id = s.id
   JOIN workflow_steps ws ON ws.workflow_id = w.id
   ORDER BY s.name, ws."order";
   ```
   You should see ASU's steps use terms like "Academic Integrity Meeting"
   and UIUC's use different terms like "Disciplinary Conference" — proving
   the schema preserves each school's own wording rather than forcing a
   shared workflow.
4. `flask run` starts without errors and `GET /api/health` returns
   `{"status": "ok"}`.

## Roadmap

- **Phase 2** — REST APIs for schools, workflows, allegations, cases,
  events, outcomes
- **Phase 3** — React (Vite) frontend: Landing, Case Setup, My Case,
  Timeline, Case Database, Resources pages
- **Phase 4** — Connect frontend to backend, test full user flow
- **Phase 5** — UI polish, validation, error handling
