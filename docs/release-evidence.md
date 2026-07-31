# Release Evidence

## Baseline

- Branch: `final-project` in the public `normalpanzer-glitch/task_tracker_complete_project` repository. The local checkout tracks `origin/final-project`.
- Date: 2026-07-31.
- Local app run command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`.
- `/health` result: `Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing` returned HTTP 200 with `{"status":"ok"}`.
- Frontend check: `python -m http.server 5500 --directory frontend` served `http://127.0.0.1:5500` with HTTP 200. The response contained the Kanban title, `New Task`, `Edit Task`, and the To Do/In Progress/Done columns.
- Test command: `python -m pytest tests -v`.
- Test result: 32 passed, 3 deprecation warnings, 0 failed on Python 3.12.13 with pytest 8.4.2 after the final release artifacts were added.

## CI Evidence

- Workflow file: `.github/workflows/ci.yml`.
- Latest confirmed green run: [CI run 30635361979](https://github.com/normalpanzer-glitch/task_tracker_complete_project/actions/runs/30635361979) completed successfully on `final-project`; both `Python tests` and `Docker smoke test` passed. Current branch runs are available from the [CI workflow page](https://github.com/normalpanzer-glitch/task_tracker_complete_project/actions/workflows/ci.yml?query=branch%3Afinal-project).
- Test command used by CI: `python -m pytest tests -v`.
- Docker smoke check used by CI: build `task-tracker-final`, start `task-tracker-final-check`, and require `http://127.0.0.1:8000/health` to succeed with `curl --fail`.
- Shortcut check: no `continue-on-error`, no `|| true`, no `--exit-zero`, pytest is not skipped, Python version is pinned to `3.12`, and dependencies are installed from `requirements.txt`.

## Docker Evidence

- Build command: `docker build -t task-tracker-final .`.
- Run command: `docker run --rm -d --name task-tracker-final-check -p 8000:8000 task-tracker-final`.
- `/health` check: `Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing`, expecting HTTP 200 and `{"status":"ok"}`.
- Stop command: `docker stop task-tracker-final-check`; `--rm` removes the stopped container.
- Local Docker note: Docker CLI 29.6.2 was installed and the commands were attempted, but Docker Desktop could not start because virtualization support was not detected. A successful local container run is therefore not claimed. The linked green GitHub Actions run provides reproducible build/run/health verification on an Ubuntu runner.
- Non-root check: `Dockerfile` creates `appuser` and runs the app with `USER appuser`.
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, `.git/`, local virtual environments, caches, docs, tests, and frontend files. The `Dockerfile` copies only `requirements.txt` and `app/`.
- Runtime command: `CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`.

## Documentation Claim-Vs-Reality Log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `/health` returns `{"status":"ok"}` with HTTP 200. | `app/main.py`, `tests/test_tasks.py::test_health`, and local `Invoke-WebRequest` result. | Confirmed. | README final section includes the expected response. |
| The full test suite runs with pytest. | `requirements.txt`, `tests/test_tasks.py`, and local `python -m pytest tests -v` output. | Confirmed: 32 passed. | README and CI use the same pytest command. |
| CI installs dependencies and runs tests without hidden shortcuts. | `.github/workflows/ci.yml` review and the linked green Actions run. | Confirmed: setup-python 3.12, pip install, pytest. | Added workflow and recorded its public run. |
| Docker builds, starts, and serves `/health` without copying secrets or running as root. | Green Docker smoke-test job in CI run 30635361979, `.dockerignore`, and `Dockerfile`. | Confirmed in CI: the image built, the container started, and `curl --fail` accepted `/health`. Local Docker was blocked by unavailable virtualization. | Added a Docker smoke-test job, narrow build context, and non-root `appuser`. |
| The frontend still contains the Kanban board/create-edit flow. | `frontend/index.html` source review and local `http.server` HTTP 200 response. | Confirmed: To Do, In Progress, Done columns, New Task button, Edit modal, create/update/delete handlers. | No frontend changes made. |
