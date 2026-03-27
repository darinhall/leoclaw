"""
Thin HTTP wrapper around the orchestrator's /client/* endpoints.
"""
from __future__ import annotations

import os
from typing import Optional

import httpx

from shared.schemas import Observation, Task
from shared.utils import get_logger

logger = get_logger(__name__)

ORCHESTRATOR_BASE_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")


class OrchestratorTransport:
    def __init__(self, base_url: str = ORCHESTRATOR_BASE_URL) -> None:
        self._base = base_url.rstrip("/")
        self._client = httpx.Client(timeout=10.0)

    def poll(self) -> Optional[Task]:
        try:
            resp = self._client.get(f"{self._base}/client/poll")
            resp.raise_for_status()
            data = resp.json()
            raw = data.get("task")
            if raw is None:
                return None
            return Task(**raw)
        except httpx.HTTPError as exc:
            logger.warning("Poll failed: %s", exc)
            return None

    def send_observation(self, obs: Observation) -> bool:
        try:
            resp = self._client.post(
                f"{self._base}/client/observe",
                content=obs.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
            return True
        except httpx.HTTPError as exc:
            logger.warning("send_observation failed: %s", exc)
            return False

    def close(self) -> None:
        self._client.close()
