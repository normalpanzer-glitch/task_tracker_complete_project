from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str | None = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: str | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank")
        if len(value) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        return value

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value: str | None) -> str:
        return "" if value is None else value


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee: str | None = None
    due_date: date | None = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Title cannot be null")
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank")
        if len(value) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        return value

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value: TaskStatus | None) -> TaskStatus | None:
        if value is None:
            raise ValueError("Status cannot be null")
        return value

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value: str | None) -> str:
        return "" if value is None else value


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: str | None
    due_date: date | None
    created_at: datetime
    updated_at: datetime
