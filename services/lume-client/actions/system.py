from __future__ import annotations

import os
import time

from shared.schemas import Action, ActionResult
from shared.utils import get_logger

logger = get_logger(__name__)
MOCK = os.getenv("MOCK_ACTIONS", "true").lower() == "true"


def screenshot_action(action: Action) -> ActionResult:
    from capture import capture_screen
    path, b64 = capture_screen()
    return ActionResult(success=True, action=action, output={"screenshot_b64": b64, "path": path})


def wait(action: Action) -> ActionResult:
    seconds = action.payload.get("seconds", 1)
    logger.info("[%s] wait %ss", "MOCK" if MOCK else "REAL", seconds)
    time.sleep(seconds)
    return ActionResult(success=True, action=action)
