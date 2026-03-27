"""
Step 5: Browser actions.

MOCK_ACTIONS=true  → log only (safe to run anywhere, no GUI needed).
MOCK_ACTIONS=false → use pyautogui / playwright for real execution inside Lume.
"""
from __future__ import annotations

import os
import time

from shared.schemas import Action, ActionResult
from shared.utils import get_logger

logger = get_logger(__name__)
MOCK = os.getenv("MOCK_ACTIONS", "true").lower() == "true"


def navigate(action: Action) -> ActionResult:
    url = action.payload.get("url", "")
    if MOCK:
        logger.info("[MOCK] navigate → %s", url)
        return ActionResult(success=True, action=action, output={"url": url})
    # Real: open browser or send to playwright page
    raise NotImplementedError("Real navigation not implemented yet — set MOCK_ACTIONS=true")


def click(action: Action) -> ActionResult:
    selector = action.payload.get("selector", "")
    if MOCK:
        logger.info("[MOCK] click → %s", selector)
        return ActionResult(success=True, action=action, output={"selector": selector})
    raise NotImplementedError("Real click not implemented yet")


def type_text(action: Action) -> ActionResult:
    text = action.payload.get("text", "")
    selector = action.payload.get("selector", "")
    if MOCK:
        logger.info("[MOCK] type %r into %s", text, selector)
        return ActionResult(success=True, action=action, output={"text": text})
    raise NotImplementedError("Real type not implemented yet")


def scroll(action: Action) -> ActionResult:
    direction = action.payload.get("direction", "down")
    amount = action.payload.get("amount", 3)
    if MOCK:
        logger.info("[MOCK] scroll %s × %s", direction, amount)
        return ActionResult(success=True, action=action)
    raise NotImplementedError("Real scroll not implemented yet")
