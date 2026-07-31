# AGENTS.md

## Project Stack

- FastAPI backend in `app/`.
- Vanilla HTML/CSS/JavaScript frontend in `frontend/index.html`.
- In-memory task storage for the course project.
- Pytest API coverage in `tests/`.

## Run And Test Commands

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
python -m http.server 5500 --directory frontend
python -m pytest tests -v
```

Docker commands:

```powershell
docker build -t task-tracker-final .
docker run --rm -d --name task-tracker-final-check -p 8000:8000 task-tracker-final
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing
docker stop task-tracker-final-check
```

## Project Rules

- Do not add final-project product features. Comments, authentication, production databases, notifications, and unrelated UI changes are out of scope.
- Treat `app/` and `frontend/` as protected. Change them only for a small bug fix, security fix, or documentation-supported correction, and explain the change in `docs/final-ai-review.md`.
- Keep secrets out of prompts, docs, tests, Docker images, and Git history. Never paste tokens, `.env` values, production logs, or real personal/customer data.
- Keep release work in repo-root artifacts: README, CI, Docker files, and `docs/`.
- Prefer exact commands and real test output over broad claims.

## Docs-First Guardrails

- Read `README.md`, `requirements.txt`, `tests/`, and the relevant `app/` files before suggesting release changes.
- Check generated documentation against actual files, commands, endpoints, and test results.
- Record what was verified and what could not be verified locally.
- Reject AI suggestions that introduce new features, hide failures, skip tests, or use dangerous CI shortcuts.
