# Final AI Review and Ownership Evidence

## AGENTS.md Guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected app/frontend edits rule included: yes.

## AI Code Review Mini-Log

Reviewed diff/file: `Dockerfile`.

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Add a non-root runtime user instead of running Uvicorn as root. | Useful | It reduces container privilege if the API process is compromised. | Implemented `useradd ... appuser` and `USER appuser`. |
| Copy the entire repository into the image for simplicity. | Wrong | It would copy docs, tests, frontend, and could accidentally include local-only files if `.dockerignore` is missed. | Rejected. `Dockerfile` copies only `requirements.txt` and `app/`. |
| Use `--reload` in the container command for developer convenience. | Wrong | `--reload` is a local-dev behavior, not a release runtime command. | Rejected. `CMD` uses plain Uvicorn on `0.0.0.0:8000`. |

## AI Security Mini-Review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| CORS should stay limited to the local frontend origins. | `app/main.py` allows only `http://localhost:5500` and `http://127.0.0.1:5500`. | Valid | The current config avoids wildcard origins while supporting the course frontend. | Keep as-is unless a documented frontend origin changes. |
| Extra request fields should be rejected so clients cannot set server-managed task fields. | `app/models.py` uses `ConfigDict(extra="forbid")`; `tests/test_tasks.py::test_create_rejects_extra_and_server_fields` covers `id`. | Valid | This protects server-owned fields like `id`, `created_at`, and `updated_at`. | Keep tests in CI. |
| In-memory storage is not production-safe. | `app/storage.py` stores tasks in module-level `_tasks`; README states tasks reset on restart. | Valid | It is acceptable for course scope but not durable or multi-process safe. | Documented scope; do not add a database for final project. |
| Missing authentication is a critical vulnerability. | No auth code exists in `app/main.py`. | Noise | Authentication is explicitly out of final-project scope and the app is a local course project. | Do not add auth as a final-project feature. |

## Manual Security Check

I manually checked that no `.env` file or secret values are required by the app, tests, CI, or Dockerfile. The runtime uses only package dependencies and in-memory storage, and `.dockerignore` excludes `.env` and `.env.*` so local secrets are not baked into the Docker context.

## One AI Output I Rejected Or Corrected

I corrected stale release evidence after confirming that the public `final-project` branch and a successful GitHub Actions run exist. I also refused to claim a successful local Docker run: Docker Desktop could not start because this laptop did not report virtualization support. Instead, the limitation is recorded explicitly and CI performs a Docker build/run/health smoke test that fails loudly if the container is not healthy.

## Three AI Usage Rules

1. Never paste: secrets, `.env` values, tokens, real customer data, private production logs, or personal data.
2. Always verify: run tests or a targeted command, inspect the diff, and check AI claims against real files before accepting them.
3. Record AI contributions by: naming the changed file, grading useful/noisy/wrong suggestions, and writing down rejected or corrected suggestions.

## Ownership Statement

I am comfortable submitting this repo as my own work because the final changes are release artifacts that I can explain file by file. I checked the actual backend, frontend, tests, and assignment brief before accepting the generated documentation. I ran the pytest suite and a real local `/health` request instead of relying only on AI text. I also rejected AI-style shortcuts that would add product features or claim unavailable verification results.
