from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal: str
    steps: List[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)


class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus
    observations: List["Observation"] = Field(default_factory=list)
    error: Optional[str] = None
    completed_at: Optional[datetime] = None


# Avoid circular import — import lazily at type-check time
from .observation import Observation  # noqa: E402
TaskResult.model_rebuild()
