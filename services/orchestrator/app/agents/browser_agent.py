"""
BrowserAgent: high-level workflow that wraps plan → execute → observe.

Think of this as the "skill" layer — specific, reusable end-to-end behaviours
built on top of the planner and executor primitives.
"""
from __future__ import annotations

from shared.schemas import Task, TaskResult, TaskStatus
from shared.utils import get_logger

from ..executor import Executor
from ..planner import plan

logger = get_logger(__name__)


class BrowserAgent:
    def __init__(self, executor: Executor) -> None:
        self._executor = executor

    async def run(self, goal: str) -> TaskResult:
        steps = plan(goal)
        task = Task(goal=goal, steps=steps)

        logger.info("BrowserAgent starting task %s", task.id)
        self._executor.enqueue(task)

        observations = await self._executor.wait_for_result(task.id)
        status = TaskStatus.COMPLETED if observations else TaskStatus.FAILED

        return TaskResult(
            task_id=task.id,
            status=status,
            observations=observations,
        )
