"""
Routes used exclusively by the lume-client.

GET  /client/poll     — lume-client asks "any work for me?"
POST /client/observe  — lume-client sends back an Observation
"""
from __future__ import annotations

from fastapi import APIRouter

from shared.schemas import Observation
from shared.utils import get_logger

from ..executor.executor import Executor

logger = get_logger(__name__)
router = APIRouter(prefix="/client", tags=["client"])


def get_executor() -> Executor:
    from ..main import executor
    return executor


@router.get("/poll")
def poll_task() -> dict:
    task = Executor.pop_task()
    if task is None:
        return {"task": None}
    logger.info("Dispatching task %s to lume-client", task.id)
    return {"task": task.model_dump()}


@router.post("/observe", status_code=204)
def receive_observation(obs: Observation) -> None:
    Executor.record_observation(obs)
    logger.debug("Observation received for task %s step %d", obs.task_id, obs.step_index)
