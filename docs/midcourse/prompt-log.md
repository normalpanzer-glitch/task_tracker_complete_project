# AI Prompt Log

## Feature 1: Due dates and overdue filtering

### Prompt 1 - weak, not applied

> Add due dates to my task tracker.

The prompt left validation, overdue meaning, API shape, and frontend behavior unspecified. Its likely output would be difficult to verify.

### Prompt 2 - rewritten strong prompt

> Add optional `due_date` support to the existing Pydantic v2 TaskCreate, TaskUpdate, and TaskResponse models. Preserve extra-field rejection and all server-managed fields. Extend existing in-memory storage and GET `/tasks` with optional `overdue: bool`. Define overdue as due_date before today and status not Done. Do not add a database or new endpoint. Add focused tests for valid/invalid dates, update preservation, and overdue filtering.

Accepted: native Pydantic date validation, computed overdue logic, focused tests. Edited: explicitly excluded Done tasks. Rejected: database persistence and stored overdue flags.

### Prompt 3 - frontend integration

> Add a native date input to the existing create/edit modal, include changed due_date values in POST/PATCH payloads, display due dates on cards, and visually mark unfinished past-due tasks. Add an overdue-only control that calls GET `/tasks?overdue=true`. Preserve drag/drop, sorting, and empty columns.

Accepted: native date input and card badges. Edited: kept DOM text assignment rather than unsafe HTML insertion. Rejected: date-picker libraries.

## Feature 2: Search and combined filters

### Prompt 1 - weak, not applied

> Add search and filters.

The prompt did not define searchable fields, combination semantics, API parameters, or empty behavior.

### Prompt 2 - rewritten strong prompt

> Extend existing GET `/tasks` with optional `search` and `assignee` query parameters. Search title and description case-insensitively. Match assignee case-insensitively and exactly after trimming. Combine search, assignee, status, priority, and overdue using AND semantics. Return 200 with `[]` for no matches. Do not create a new endpoint or dependency.

Accepted: one composable list endpoint and case-insensitive matching. Edited: constrained searchable fields. Rejected: fuzzy matching and full-text indexes.

### Prompt 3 - frontend controls

> Add a compact search/filter bar above the board with text search, priority, assignee, overdue-only, and Clear. Debounce text search by 300 ms. Build URLSearchParams safely. Preserve all three columns and existing loading/error states.

Accepted: URLSearchParams, debounce, Clear action. Edited: used change events for non-search controls to reduce unnecessary requests. Rejected: saved views and frontend frameworks.
