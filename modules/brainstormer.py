from __future__ import annotations

import json
import logging
import re
import google.generativeai as genai
from typing import Any


def _extract_json_array(text: str) -> str | None:
    """Best-effort extraction of a JSON array substring from free-form text."""
    # Strip code fences if present
    fenced = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", text.strip())
    if fenced.startswith("[") and fenced.endswith("]"):
        return fenced
    # Find first [ ... ] block
    m = re.search(r"\[[\s\S]*\]", fenced)
    return m.group(0) if m else None


def brainstorm_themes(topic: str, model: Any) -> list[str] | None:
    """Generate 5 themes for the given topic.

    Args:
        topic: High-level topic (e.g., "The Dune Novels").
        model: Configured GenerativeModel instance.

    Returns:
        A list of 5 theme strings, or None if generation/parsing failed.
    """
    print(f"\n🧠 Brainstorming themes for: {topic}...")

    prompt = (
        "You are assisting with a video essay.\n"
        f"Topic: {topic}\n"
        "Return exactly 5 concise theme sentences as a strict JSON array of strings.\n"
        "Example: [\"Theme 1.\", \"Theme 2.\", \"Theme 3.\", \"Theme 4.\", \"Theme 5.\"]\n"
        "Do not include any commentary outside the JSON."
    )

    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip() if resp else ""
        arr_str = _extract_json_array(text)
        if not arr_str:
            logging.warning("Brainstormer: no JSON array found in response")
            return None
        themes = json.loads(arr_str)
        if not (isinstance(themes, list) and all(isinstance(t, str) and t.strip() for t in themes)):
            logging.warning("Brainstormer: invalid themes structure")
            return None
        print("✅ Brainstorming complete.")
        return themes
    except json.JSONDecodeError as e:
        logging.warning("Brainstormer: JSON parse error: %s", e)
        return None
    except Exception as e:
        logging.warning("Brainstormer: generation error: %s", e)
        return None

