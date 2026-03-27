"""
POST /task   — submit a goal
GET  /task/{id} — check status / retrieve observations
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from shared.schemas import Task, TaskResult, TaskStatus
from shared.utils import get_logger

from ..executor import Executor
from ..planner import plan

logger = get_logger(__name__)
router = APIRouter(prefix="/task", tags=["tasks"])


class CreateTaskRequest(BaseModel):
    goal: str


def get_executor() -> Executor:
    # Imported here to avoid circular deps; replaced with DI in Step 9+
    from ..main import executor
    return executor


@router.post("", status_code=202)
def create_task(
    req: CreateTaskRequest,
    executor: Executor = Depends(get_executor),
) -> dict:
    steps = plan(req.goal)
    task = Task(goal=req.goal, steps=steps)
    executor.enqueue(task)
    logger.info("Task %s created: %r", task.id, task.goal)
    return {"status": "received", "task_id": task.id, "steps": task.steps}


@router.get("/{task_id}")
def get_task_result(
    task_id: str,
    executor: Executor = Depends(get_executor),
) -> dict:
    from ..executor.executor import _results
    if task_id not in _results:
        raise HTTPException(status_code=404, detail="Task not found")
    observations = _results[task_id]
    done = bool(observations and observations[-1].metadata.get("done"))
    return {
        "task_id": task_id,
        "observation_count": len(observations),
        "done": done,
        "observations": [o.model_dump() for o in observations],
    }
