# Release Evidence

## Baseline

- Branch: `final-project` target branch. This local Codex folder is not currently a Git worktree, so create/push the branch in the public repository before submission.
- Date: 2026-07-28.
- Local app run command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`.
- `/health` result: `Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing` returned HTTP 200 with `{"status":"ok"}`.
- Frontend check: `python -m http.server 5500 --directory frontend` served `http://127.0.0.1:5500` with HTTP 200. The response contained the Kanban title, `New Task`, `Edit Task`, and the To Do/In Progress/Done columns.
- Test command: `python -m pytest tests -v`.
- Test result: 32 passed, 3 deprecation warnings, 0 failed on Python 3.12.13 with pytest 8.4.2 after the final release artifacts were added.

## CI Evidence

- Workflow file: `.github/workflows/ci.yml`.
- Latest run link or note: no GitHub Actions run link is available from this local non-git workspace yet. The workflow should run after pushing the `final-project` branch to the public GitHub repository.
- Test command used by CI: `python -m pytest tests -v`.
- Shortcut check: no `continue-on-error`, no `|| true`, pytest is not skipped, Python version is pinned to `3.12`, and dependencies are installed from `requirements.txt`.

## Docker Evidence

- Build command: `docker build -t task-tracker-final .`.
- Run command: `docker run --rm -p 8000:8000 task-tracker-final`.
- `/health` check: `Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing`, expecting HTTP 200 and `{"status":"ok"}`.
- Local Docker note: Docker could not be run in this workspace because `docker` is not installed or not on PATH (`The term 'docker' is not recognized`). Run the commands above on a machine with Docker Desktop before final submission if possible.
- Non-root check: `Dockerfile` creates `appuser` and runs the app with `USER appuser`.
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, `.git/`, local virtual environments, caches, docs, tests, and frontend files. The `Dockerfile` copies only `requirements.txt` and `app/`.
- Runtime command: `CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`.

## Documentation Claim-Vs-Reality Log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `/health` returns `{"status":"ok"}` with HTTP 200. | `app/main.py`, `tests/test_tasks.py::test_health`, and local `Invoke-WebRequest` result. | Confirmed. | README final section includes the expected response. |
| The full test suite runs with pytest. | `requirements.txt`, `tests/test_tasks.py`, and local `python -m pytest tests -v` output. | Confirmed: 32 passed. | README and CI use the same pytest command. |
| CI installs dependencies and runs tests without hidden shortcuts. | `.github/workflows/ci.yml` review. | Confirmed: setup-python 3.12, pip install, pytest. | Added workflow. |
| Docker does not copy secrets and runs as non-root. | `.dockerignore` and `Dockerfile` review. | Confirmed by file review; local Docker runtime not available. | Added `.dockerignore` and non-root `appuser`. |
| The frontend still contains the Kanban board/create-edit flow. | `frontend/index.html` source review and local `http.server` HTTP 200 response. | Confirmed: To Do, In Progress, Done columns, New Task button, Edit modal, create/update/delete handlers. | No frontend changes made. |
