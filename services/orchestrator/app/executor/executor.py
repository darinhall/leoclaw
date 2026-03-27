"""
Responsible for dispatching a Task to the lume-client and collecting Observations.

Current implementation: in-memory queue (no network).
Step 4+: replace the queue with an HTTP call / Redis pub-sub to the real Lume VM.
"""
from __future__ import annotations

import asyncio
from collections import deque
from typing import Deque, Dict, Optional

from shared.schemas import Observation, Task, TaskStatus
from shared.utils import get_logger

logger = get_logger(__name__)

# Single global task queue — lume-client polls this
_task_queue: Deque[Task] = deque()
_results: Dict[str, list[Observation]] = {}


class Executor:
    def enqueue(self, task: Task) -> None:
        logger.info("Enqueuing task %s — %r", task.id, task.goal)
        _task_queue.append(task)
        _results[task.id] = []

    async def wait_for_result(
        self, task_id: str, timeout_s: float = 60.0
    ) -> list[Observation]:
        """Poll until lume-client signals completion or timeout fires."""
        deadline = asyncio.get_event_loop().time() + timeout_s
        while asyncio.get_event_loop().time() < deadline:
            obs = _results.get(task_id, [])
            if obs and obs[-1].metadata.get("done"):
                return obs
            await asyncio.sleep(0.5)
        logger.warning("Timeout waiting for task %s", task_id)
        return _results.get(task_id, [])

    # ── called by lume-client (via route) ──────────────────────────────────

    @staticmethod
    def pop_task() -> Optional[Task]:
        """Return the next pending task, or None if the queue is empty."""
        return _task_queue.popleft() if _task_queue else None

    @staticmethod
    def record_observation(obs: Observation) -> None:
        if obs.task_id in _results:
            _results[obs.task_id].append(obs)
            logger.debug(
                "Observation recorded for task %s (step %d)", obs.task_id, obs.step_index
            )
        else:
            logger.warning("Received observation for unknown task %s", obs.task_id)
