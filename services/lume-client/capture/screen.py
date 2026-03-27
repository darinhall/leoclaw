"""
Step 6: Screenshot capture.

In mock mode (MOCK_ACTIONS=true) returns a placeholder.
In real mode uses `pyautogui` or `playwright` to grab the screen.
"""
from __future__ import annotations

import base64
import os
from pathlib import Path

from shared.constants import DEFAULT_SCREENSHOT_DIR
from shared.utils import get_logger

logger = get_logger(__name__)
MOCK = os.getenv("MOCK_ACTIONS", "true").lower() == "true"


def capture_screen(save_dir: str = DEFAULT_SCREENSHOT_DIR) -> tuple[str | None, str | None]:
    """
    Returns (file_path, base64_string).
    base64 is used for immediate transport back to orchestrator.
    """
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    if MOCK:
        logger.debug("MOCK capture — returning placeholder")
        placeholder = b"MOCK_SCREENSHOT_BYTES"
        b64 = base64.b64encode(placeholder).decode()
        return None, b64

    try:
        import pyautogui  # type: ignore
        from datetime import datetime

        filename = f"screenshot_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.png"
        path = os.path.join(save_dir, filename)
        pyautogui.screenshot(path)
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        logger.debug("Screenshot saved to %s", path)
        return path, b64
    except Exception as exc:
        logger.error("Screenshot failed: %s", exc)
        return None, None
