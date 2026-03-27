from __future__ import annotations

import os

from shared.schemas import Action, ActionResult
from shared.utils import get_logger

logger = get_logger(__name__)
MOCK = os.getenv("MOCK_ACTIONS", "true").lower() == "true"


def keypress(action: Action) -> ActionResult:
    key = action.payload.get("key", "")
    if MOCK:
        logger.info("[MOCK] keypress → %s", key)
        return ActionResult(success=True, action=action, output={"key": key})
    raise NotImplementedError("Real keypress not implemented yet")
