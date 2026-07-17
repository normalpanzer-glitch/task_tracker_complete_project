from datetime import date, datetime, timezone
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate


_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    search: str | None = None,
    assignee: str | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    normalized_search = search.strip().casefold() if search else None
    normalized_assignee = assignee.strip().casefold() if assignee else None
    today = date.today()
    results: list[TaskResponse] = []
    for task in _tasks.values():
        is_overdue = task.due_date is not None and task.due_date < today and task.status != TaskStatus.DONE
        searchable_text = f"{task.title} {task.description}".casefold()
        if status is not None and task.status != status:
            continue
        if priority is not None and task.priority != priority:
            continue
        if normalized_search and normalized_search not in searchable_text:
            continue
        if normalized_assignee and (task.assignee or "").casefold() != normalized_assignee:
            continue
        if overdue is not None and is_overdue != overdue:
            continue
        results.append(task)
    return results


def get_task_by_id(task_id: str) -> TaskResponse | None:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse | None:
    current = _tasks.get(task_id)
    if current is None:
        return None

    changes = payload.model_dump(exclude_unset=True)
    if changes:
        changes["updated_at"] = datetime.now(timezone.utc)
        current = current.model_copy(update=changes)
        _tasks[task_id] = current
    return current


def delete_task(task_id: str) -> bool:
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
