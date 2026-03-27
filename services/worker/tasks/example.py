"""Placeholder task — replace with real background jobs."""
from shared.utils import get_logger

logger = get_logger("worker.tasks.example")


async def example_task() -> None:
    logger.debug("example_task heartbeat")
