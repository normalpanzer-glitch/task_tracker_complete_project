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

## Run from VS Code

Opening `frontend/index.html` directly with `file://` cannot start the FastAPI backend. Open the **repository folder** in VS Code instead. After creating the virtual environment and installing the requirements, use:

1. **Terminal -> Run Task**
2. Choose **Start Task Tracker**
3. Open `http://localhost:5500` in a browser

The task starts the backend and frontend in two VS Code integrated terminals. Use **Terminal -> Run Task -> Run backend tests** to execute the test suite. Stop the two task terminals when you are finished.

## Test

```powershell
python -m pytest tests -v
```

Storage is intentionally in-memory for the course project, so tasks reset whenever the backend process restarts.

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- Docker image builds a FastAPI runtime for `/health` and task API verification.
- AI review, security review, and ownership evidence is in `docs/`.

### How to run locally

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Verify the API:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing
```

Run the frontend in a second terminal:

```powershell
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500` and confirm the Kanban columns plus create/edit modal are visible.

### How to run tests

```powershell
python -m pytest tests -v
```

### How to run with Docker

```powershell
docker build -t task-tracker-final .
docker run --rm -p 8000:8000 task-tracker-final
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing
```

Expected health response:

```json
{"status":"ok"}
```

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped draft and review the final-project release artifacts: CI, Docker, README, and evidence documents. I verified the work by running the pytest suite, starting the FastAPI app locally, checking `/health`, reviewing protected app/frontend files, and checking documentation claims against the actual repository. One AI suggestion I corrected was to avoid claiming Docker or GitHub Actions had already run locally, because this workspace does not have Docker available and is not currently a Git worktree.
