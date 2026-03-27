"""
Step 7: Basic rule-based planner.
Replace `_rule_based_plan` with an LLM call (Step 8) when ready.
"""
from __future__ import annotations

from typing import List

from shared.utils import get_logger

logger = get_logger(__name__)


def plan(goal: str) -> List[str]:
    """Turn a plain-language goal into an ordered list of step strings."""
    steps = _rule_based_plan(goal)
    logger.info("Planned %d steps for goal: %r", len(steps), goal)
    return steps


def _rule_based_plan(goal: str) -> List[str]:
    goal_lower = goal.lower()

    if "google" in goal_lower and "search" in goal_lower:
        query = _extract_search_query(goal_lower)
        return [
            "navigate:https://www.google.com",
            f"type:#APW_search_box:{query}",
            "keypress:Enter",
            "screenshot",
        ]

    if "navigate" in goal_lower or "open" in goal_lower or "go to" in goal_lower:
        url = _extract_url(goal_lower) or "https://example.com"
        return [f"navigate:{url}", "screenshot"]

    # Fallback: treat the whole goal as a single navigate step
    return [f"navigate:https://www.google.com", f"type:#APW_search_box:{goal}", "keypress:Enter", "screenshot"]


def _extract_search_query(text: str) -> str:
    for marker in ("search for ", "search ", "find "):
        if marker in text:
            return text.split(marker, 1)[-1].strip()
    return text


def _extract_url(text: str) -> str | None:
    for word in text.split():
        if word.startswith("http") or "." in word:
            return word if word.startswith("http") else f"https://{word}"
    return None
