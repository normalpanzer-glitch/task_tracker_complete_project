from fastapi import FastAPI, HTTPException, Response, status as http_status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)


app = FastAPI(title="Task Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=http_status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    search: str | None = None,
    assignee: str | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(
        status=status,
        priority=priority,
        search=search,
        assignee=assignee,
        overdue=overdue,
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise _task_not_found(task_id)
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    current = storage.get_task_by_id(task_id)
    if current is None:
        raise _task_not_found(task_id)
    if payload.status is not None:
        validate_status_transition(current.status, payload.status)

    updated = storage.update_task(task_id, payload)
    if updated is None:  # Defensive guard; the task was confirmed above.
        raise _task_not_found(task_id)
    return updated


@app.delete(
    "/tasks/{task_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: str) -> Response:
    if not storage.delete_task(task_id):
        raise _task_not_found(task_id)
    return Response(status_code=http_status.HTTP_204_NO_CONTENT)


def _task_not_found(task_id: str) -> HTTPException:
    return HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} not found",
    )
