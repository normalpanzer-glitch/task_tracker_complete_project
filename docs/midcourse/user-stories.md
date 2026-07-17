# Mid-Course User Stories

## Feature 1: Due dates and overdue filtering

1. As a task owner, I want to set an optional due date so that I can see when work is expected.
   - A valid ISO date is accepted on create and update.
   - An invalid date returns HTTP 422.
   - Tasks without a due date remain valid.
2. As a board user, I want due dates displayed on cards so that deadlines are visible without opening a task.
   - A dated card shows its due date.
   - A past-due unfinished task shows an Overdue badge.
3. As a board user, I want an overdue-only filter so that I can focus on late work.
   - The filter returns tasks whose due date is before today.
   - Done tasks are not considered overdue.
   - No matches returns HTTP 200 with an empty list and visible board columns.

**AI assumption corrected:** An initial design could classify every past-due task as overdue. We corrected this so completed tasks are excluded.

## Feature 2: Search and combined filters

1. As a board user, I want to search task titles and descriptions so that I can find work quickly.
   - Search is case-insensitive.
   - Partial matches are accepted.
2. As a board user, I want to combine search with priority and assignee filters so that results are precise.
   - All supplied filters are applied together using AND behavior.
   - Assignee matching is case-insensitive.
3. As a board user, I want to clear all filters with one action so that I can return to the full board.
   - Clear resets search, priority, assignee, and overdue controls.
   - All three Kanban columns remain visible when no tasks match.

**AI assumption corrected:** Search was constrained to title and description only; broad fuzzy search and new dependencies were rejected as out of scope.
