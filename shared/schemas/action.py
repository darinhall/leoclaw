from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ActionType(str, Enum):
    NAVIGATE = "navigate"      # go to a URL
    CLICK = "click"            # click an element
    TYPE = "type"              # type text into a field
    SCREENSHOT = "screenshot"  # capture current screen
    SCROLL = "scroll"          # scroll the page
    WAIT = "wait"              # pause for N seconds
    KEYPRESS = "keypress"      # send a key combo


class Action(BaseModel):
    type: ActionType
    payload: Dict[str, Any] = {}
    timeout_ms: int = 5000


class ActionResult(BaseModel):
    success: bool
    action: Action
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
