# Verification

## Baseline

The Module 1-3 project had 23 passing backend tests before feature work. Existing behavior included CRUD, strict validation, transition rules, CORS, and the Kanban frontend.

## Automated results

- Final suite: **30 passed**.
- New tests: valid due date, invalid date, due-date update preservation, overdue filtering, title/description search, combined filters, and no-match behavior.
- Frontend embedded JavaScript: syntax check passed.

## Manual browser contract

- Create a task with and without a due date.
- Edit a due date without changing status.
- Verify past-due unfinished cards show Overdue.
- Verify Done cards are not labeled overdue.
- Search by title and by description with different letter casing.
- Combine search, High priority, and assignee.
- Select overdue only.
- Clear filters and confirm the complete board returns.
- Confirm all three columns remain visible with no matches.
- Recheck create, edit, delete, priority sorting, valid drag, rejected drag rollback, and modal dismissal.

## Break Test 1: overdue behavior

Temporary source change: replaced overdue computation in `app/storage.py` with `is_overdue = False`.

Result: `test_overdue_filter_excludes_done_tasks` failed because the API returned `[]` instead of the expected overdue task. The correct computation was restored.

## Break Test 2: description search

Temporary source change: searched only `task.title` and omitted `task.description`.

Result: `test_search_matches_title_and_description` failed on the description-only query `launch`. Title-and-description search was restored.

## Post-restoration check

The full suite was rerun after restoring both source changes: **30 passed**.

## Live integration smoke test

- Frontend returned HTTP 200 and contained the due-date and search controls.
- POST created a High-priority task with due date `2026-07-19`.
- Combined `search=deadline`, `priority=High`, and `assignee=maya` returned exactly one matching task.
- DELETE cleanup returned HTTP 204.
