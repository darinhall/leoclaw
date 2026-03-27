"""
Maps an Action to the correct handler.
Add new ActionType handlers here as the system grows.
"""
from __future__ import annotations

import os

from shared.schemas import Action, ActionResult, ActionType
from shared.utils import get_logger

from . import browser, keyboard, system

logger = get_logger(__name__)
MOCK = os.getenv("MOCK_ACTIONS", "true").lower() == "true"

_HANDLERS = {
    ActionType.NAVIGATE: browser.navigate,
    ActionType.CLICK: browser.click,
    ActionType.TYPE: browser.type_text,
    ActionType.SCREENSHOT: system.screenshot_action,
    ActionType.SCROLL: browser.scroll,
    ActionType.WAIT: system.wait,
    ActionType.KEYPRESS: keyboard.keypress,
}


def dispatch(action: Action) -> ActionResult:
    handler = _HANDLERS.get(action.type)
    if handler is None:
        return ActionResult(
            success=False,
            action=action,
            error=f"No handler registered for action type: {action.type}",
        )
    try:
        return handler(action)
    except Exception as exc:
        logger.exception("Action %s failed: %s", action.type, exc)
        return ActionResult(success=False, action=action, error=str(exc))
