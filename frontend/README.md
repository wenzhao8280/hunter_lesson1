# CaseNext frontend

React (Vite, JavaScript) frontend for CaseNext. See the repo root
[README](../README.md) for what CaseNext is and overall project status.

## Pages

- **Landing** (`/`) — intro + call to action
- **Case Setup** (`/setup`) — pick your school and allegation type, creates a case
- **My Case** (`/case/:id`) — status, workflow progress, case details form
- **Timeline** (`/case/:id/timeline`) — add and view case events
- **Case Database** (`/cases`) — browse anonymized cases, filterable by school/status
- **Resources** (`/resources`) — a school's offices and official links

There's no login system yet: "my case" is just the id of the last case
Case Setup created, remembered in `localStorage` (see `src/context/CaseContext.jsx`).

## Running locally

Requires the backend running (see `../backend/README.md`).

```bash
cd frontend
npm install
cp .env.example .env
# edit .env if your backend isn't on the default http://127.0.0.1:5000/api
npm run dev
```
