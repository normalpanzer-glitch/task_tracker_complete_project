# Mini ADR: Due Dates and Combined Search Filters

## Context

The Module 1-3 Task Tracker uses FastAPI, strict Pydantic v2 models, in-memory storage, and a vanilla JavaScript Kanban board. The mid-course project requires two small end-to-end features while preserving that architecture.

## Decision

Add an optional `due_date: date | None` to task create, update, and response models. Compute overdue status during backend filtering: a task is overdue when its date is before today and its status is not Done. Add `search`, `assignee`, and `overdue` query parameters to the existing `GET /tasks`; combine them with existing status and priority filters using AND semantics.

The frontend adds a native date input, due/overdue card badges, and a compact filter bar. It continues to use the existing API and vanilla HTML/CSS/JavaScript.

## Alternatives rejected

- A database migration was rejected because the course baseline explicitly uses in-memory storage.
- A separate search endpoint was rejected because query parameters on `GET /tasks` keep the API small.
- Fuzzy-search libraries were rejected as unnecessary complexity.
- Storing a separate `is_overdue` field was rejected because it can become stale as dates and statuses change.

## Consequences

The design is small, testable, and preserves all prior behavior. Dates follow ISO `YYYY-MM-DD` parsing through Pydantic. Overdue status is always current but depends on the server's local date.
