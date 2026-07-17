# Reflection

I used Codex as a coding and review partner for planning, backend implementation, frontend integration, tests, and debugging. The most useful part was turning broad feature ideas into explicit behavior contracts. For due dates, the contract specified the exact model field, validation behavior, overdue definition, frontend display, and filter behavior before code changed. For search, it established searchable fields and AND semantics for combined filters. This made the generated changes easier to inspect and test.

AI helped most when it connected a feature across layers. Adding `due_date` was not only a model change: storage, response serialization, the modal, edit comparison logic, card rendering, API tests, and manual checks all had to agree. The structured workflow made those dependencies visible.

AI also slowed the work when environmental assumptions were wrong. The extracted virtual environment referenced a Python installation that was not available, and the extracted folder was not yet a Git repository. Those issues required evidence-based diagnosis before feature work could be verified. This reinforced that plausible setup instructions are not proof that a command works on the current machine.

My review changed two important decisions. First, completed tasks with past dates are not treated as overdue. A simple date comparison would have produced misleading results. Second, search was kept intentionally narrow: case-insensitive matching across title and description, with exact normalized assignee matching. Fuzzy search, extra libraries, a new endpoint, and database changes were rejected as unnecessary for the project scope.

The Break Tests were especially valuable. Disabling overdue detection caused the overdue test to fail for the expected reason. Removing description text from search caused the description-query assertion to fail. Restoring the implementation returned the full suite to green. This showed that the new tests protect actual feature behavior rather than merely exercising endpoints. AI produced drafts and suggestions, but the acceptance criteria, corrections, verification, and final ownership remained mine.
