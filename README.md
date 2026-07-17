# Task Tracker Kanban

This repository contains the Module 2 FastAPI backend and Module 3 vanilla JavaScript Kanban frontend.

## Mid-course features

- Optional task due dates with due/overdue card badges and overdue-only filtering.
- Case-insensitive title/description search combined with priority and assignee filters.
- Mid-course workflow evidence is in `docs/midcourse/`.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the backend

From the repository root:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Verify [http://localhost:8000/health](http://localhost:8000/health), [http://localhost:8000/tasks](http://localhost:8000/tasks), or [http://localhost:8000/docs](http://localhost:8000/docs).

## Run the frontend

In a second terminal:

```powershell
python -m http.server 5500 --directory frontend
```

Open [http://localhost:5500](http://localhost:5500). CORS is configured for both `localhost:5500` and `127.0.0.1:5500`.

## Test

```powershell
python -m pytest tests -v
```

Storage is intentionally in-memory for the course project, so tasks reset whenever the backend process restarts.
