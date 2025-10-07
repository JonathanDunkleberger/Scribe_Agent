from __future__ import annotations

import json
import logging
import re
import google.generativeai as genai
from typing import Any


def _extract_json_array(text: str) -> str | None:
    fenced = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", text.strip())
    if fenced.startswith("[") and fenced.endswith("]"):
        return fenced
    m = re.search(r"\[[\s\S]*\]", fenced)
    return m.group(0) if m else None


def create_outline(topic: str, theme: str, model: Any, sections: int = 8) -> list[str] | None:
    """Create a structured outline for the topic and theme.

    Args:
        topic: High-level topic.
        theme: Selected theme.
        model: Configured GenerativeModel.
        sections: Target number of sections (1-12).

    Returns:
        List of section strings, or None on failure.
    """
    print(f"\n📝 Creating a {sections}-part outline for the theme: '{theme}'...")

    sections = max(1, min(12, sections))
    prompt = (
        f"Create a detailed, {sections}-part outline for a video essay.\n"
        f"Topic: {topic}\nTheme: {theme}\n"
        "Return a strict JSON array of strings with exactly the number of sections requested.\n"
        "No commentary outside the JSON."
    )

    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip() if resp else ""
        arr_str = _extract_json_array(text)
        if not arr_str:
            logging.warning("Outliner: no JSON array found in response")
            return None
        outline = json.loads(arr_str)
        if not (isinstance(outline, list) and all(isinstance(s, str) and s.strip() for s in outline)):
            logging.warning("Outliner: invalid outline structure")
            return None
        print("✅ Outline created successfully.")
        return outline
    except json.JSONDecodeError as e:
        logging.warning("Outliner: JSON parse error: %s", e)
        return None
    except Exception as e:
        logging.warning("Outliner: generation error: %s", e)
        return None
