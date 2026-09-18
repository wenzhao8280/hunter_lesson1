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

## Status: Phase 3 — Frontend connected to the backend

Done so far:

**Phase 1 — Backend foundation**
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

**Phase 2 — REST API**
- `GET /api/schools`, `GET /api/schools/<id>`
- `GET /api/schools/<id>/offices`
- `GET /api/schools/<id>/terminology`
- `GET /api/schools/<id>/workflows` (each workflow includes its ordered
  steps)
- `GET /api/schools/<id>/allegation-types`
- `GET /api/schools/<id>/resources`
- `POST /api/cases`, `GET /api/cases` (filter with `?school_id=` /
  `?status=`), `GET /api/cases/<id>`, `PATCH /api/cases/<id>`
- `PUT /api/cases/<id>/details`
- `GET /api/cases/<id>/events`, `POST /api/cases/<id>/events`
- `GET /api/cases/<id>/outcomes`, `POST /api/cases/<id>/outcomes`

All write endpoints validate required fields, that foreign keys exist and
belong to the right school/workflow, and that dates are valid ISO 8601 —
returning a JSON `{"error": "..."}` body with a 400/404 status rather than
a raw 500.

**Phase 3 — React (Vite) frontend**
- Six pages, wired to the live API: Landing, Case Setup, My Case (status +
  workflow progress + details form), Timeline (add/view events), Case
  Database (browse/filter other cases), Resources (a school's offices and
  links)
- No login system yet — "my case" is just the id of the case Case Setup
  last created, remembered in the browser's `localStorage`
- End-to-end tested against the real backend with a headless-browser
  script (create a case, advance its workflow step, save details, add a
  timeline event, browse the case database, view resources) — see
  `frontend/README.md`

Not built yet (later phases): user accounts, AI features, deeper UI
polish (Phase 5).

## Project structure

```
backend/
  app/
    __init__.py        # Flask app factory
    config.py           # Configuration (reads DATABASE_URL etc. from .env)
    extensions.py        # Shared db/migrate instances
    models/              # One file per database table
    routes/               # REST API endpoints
  migrations/            # Flask-Migrate / Alembic migration history
  seed.py                # Populates sample schools/cases for local dev
  run.py                 # App entry point
  requirements.txt
  .env.example           # Copy to .env and fill in DB credentials

frontend/
  src/
    api.js                # Fetch wrapper for the backend REST API
    context/               # "My case" id, remembered via localStorage
    components/            # NavBar, StepProgress, status banners
    pages/                  # Landing, CaseSetup, MyCase, Timeline,
                            # CaseDatabase, Resources
  .env.example            # Copy to .env; sets VITE_API_BASE_URL
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

## Running the frontend locally

Requirements: Node.js 18+, and the backend running (above).

```bash
cd frontend
npm install
cp .env.example .env
# edit .env if your backend isn't on the default http://127.0.0.1:5000/api
npm run dev
```

Visit the URL Vite prints (typically `http://localhost:5173`).

## What to test

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
5. `GET /api/schools` returns the two seeded schools, and
   `GET /api/schools/1/workflows` returns that school's steps in order.
6. `POST /api/cases` with a valid `school_id`/`workflow_id`/
   `allegation_type_id` creates a case; `GET /api/cases/<id>` returns it
   with nested school/workflow/allegation_type/details/events/outcomes.
7. `PUT /api/cases/<id>/details`, `POST /api/cases/<id>/events`, and
   `POST /api/cases/<id>/outcomes` each add data that then shows up on
   `GET /api/cases/<id>`.
8. Sending a bad foreign key (e.g. a `workflow_id` from a different
   school) or a malformed date returns a 400 with a JSON `error` message,
   not a stack trace.
9. With both servers running: Case Setup creates a case and redirects to
   My Case; the workflow steps render and "Start first step" /
   "Mark current step complete" advances through them; the case details
   form saves and shows "Saved."; Timeline lets you add an event and see
   it in the list; Case Database lists cases and its school/status
   filters narrow the list; Resources shows offices and links once a
   school is selected (auto-selected if you have a case).

## Roadmap

- ~~**Phase 2** — REST APIs for schools, workflows, allegations, cases,
  events, outcomes~~ done
- ~~**Phase 3** — React (Vite) frontend: Landing, Case Setup, My Case,
  Timeline, Case Database, Resources pages, connected to the backend and
  tested end-to-end~~ done
- **Phase 4** — User accounts (cases currently aren't tied to a real
  user — "my case" is just remembered locally)
- **Phase 5** — UI polish, AI features
