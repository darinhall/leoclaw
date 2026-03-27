"""
Async worker — Step 7+.

Right now this is a simple polling loop.
Replace the queue with Redis / Celery / ARQ when you need horizontal scale.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared.utils import get_logger
from tasks.example import example_task

logger = get_logger("worker")

POLL_INTERVAL_S = 5.0


async def run() -> None:
    logger.info("Worker started")
    while True:
        try:
            await example_task()
        except Exception as exc:
            logger.error("Task failed: %s", exc)
        await asyncio.sleep(POLL_INTERVAL_S)


if __name__ == "__main__":
    asyncio.run(run())
