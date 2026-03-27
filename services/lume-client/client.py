"""
LeoClaw Lume Client — runs inside the Lume VM.

Loop:
  1. Poll orchestrator for a task
  2. Execute each step as an Action
  3. Capture screenshot after each step
  4. Send Observation back to orchestrator
  5. Repeat
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

# Allow importing shared/ from the repo root when running directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import os

from shared.constants import ORCHESTRATOR_TASK_POLL_INTERVAL_S
from shared.schemas import Action, ActionType, Observation, Task
from shared.utils import get_logger

from actions import dispatch
from capture import capture_screen
from transport import OrchestratorTransport

logger = get_logger("lume-client")

MOCK = os.getenv("MOCK_ACTIONS", "true").lower() == "true"


def _step_to_action(step: str) -> Action:
    """
    Parse a step string into a typed Action.

    Step format examples:
      "navigate:https://google.com"
      "type:#APW_search_box:cats"
      "keypress:Enter"
      "screenshot"
      "wait:2"
    """
    parts = step.split(":", 2)
    verb = parts[0].lower()

    if verb == "navigate":
        return Action(type=ActionType.NAVIGATE, payload={"url": parts[1] if len(parts) > 1 else ""})

    if verb == "type":
        selector = parts[1] if len(parts) > 1 else ""
        text = parts[2] if len(parts) > 2 else ""
        return Action(type=ActionType.TYPE, payload={"selector": selector, "text": text})

    if verb == "click":
        return Action(type=ActionType.CLICK, payload={"selector": parts[1] if len(parts) > 1 else ""})

    if verb == "keypress":
        return Action(type=ActionType.KEYPRESS, payload={"key": parts[1] if len(parts) > 1 else ""})

    if verb == "scroll":
        return Action(type=ActionType.SCROLL, payload={"direction": parts[1] if len(parts) > 1 else "down"})

    if verb == "wait":
        return Action(type=ActionType.WAIT, payload={"seconds": int(parts[1]) if len(parts) > 1 else 1})

    # Default to screenshot
    return Action(type=ActionType.SCREENSHOT, payload={})


def execute_task(task: Task, transport: OrchestratorTransport) -> None:
    logger.info("Starting task %s — %r (%d steps)", task.id, task.goal, len(task.steps))

    for i, step in enumerate(task.steps):
        logger.info("  Step %d/%d: %s", i + 1, len(task.steps), step)
        action = _step_to_action(step)
        result = dispatch(action)

        if not result.success:
            logger.error("  Step failed: %s", result.error)

        # Capture screen after every action
        path, b64 = capture_screen()
        is_last = i == len(task.steps) - 1

        obs = Observation(
            task_id=task.id,
            step_index=i,
            screenshot_path=path,
            screenshot_b64=b64,
            text=step,
            metadata={"done": is_last, "action_success": result.success},
        )
        transport.send_observation(obs)

    logger.info("Task %s complete", task.id)


def run_loop(poll_interval: float = ORCHESTRATOR_TASK_POLL_INTERVAL_S) -> None:
    transport = OrchestratorTransport()
    logger.info("Lume client started (MOCK=%s) — polling every %ss", MOCK, poll_interval)

    try:
        while True:
            task = transport.poll()
            if task is not None:
                execute_task(task, transport)
            else:
                logger.debug("No tasks — sleeping %ss", poll_interval)
                time.sleep(poll_interval)
    except KeyboardInterrupt:
        logger.info("Lume client stopped by user")
    finally:
        transport.close()


if __name__ == "__main__":
    run_loop()
