from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Observation(BaseModel):
    task_id: str
    step_index: int = 0
    screenshot_path: Optional[str] = None
    screenshot_b64: Optional[str] = None   # base64 for in-memory transport
    text: Optional[str] = None             # OCR or page text
    url: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)
