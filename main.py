#!/usr/bin/env python3
"""
Scribe Agent - Video Essay Script Generator

A tool for generating long-form video essay scripts using AI.
Generates compelling, personal video essays with structured outlines
and first-person narrative style.

Usage:
    python main.py [--check] [--topic TOPIC] [--sections N] [--theme-index I]

Requirements:
    - Google AI API key set as GOOGLE_API_KEY environment variable (can be in .env)
    - Internet connection for API calls

Author: Scribe Agent
Version: 1.1.0
"""

from __future__ import annotations

import argparse
import logging
import sys

from config import setup_model
from modules.brainstormer import brainstorm_themes
from modules.outliner import create_outline
from modules.drafter import draft_section
from modules.file_manager import save_script


class OfflineMockModel:
    """Simple mock to emulate generate_content() for offline mode."""

    def __init__(self) -> None:
        self._counter = 0

    class _Resp:
        def __init__(self, text: str) -> None:
            self.text = text

    def generate_content(self, prompt: str):  # type: ignore[override]
        self._counter += 1
        # naive branching to supply deterministic JSON for brainstorming/outline
        if 'Return exactly 5 concise theme sentences' in prompt:
            return self._Resp('["A thematic exploration of the core ideas.", "Character development across arcs.", "Socio-political commentary embedded in narrative.", "Stylistic evolution and tonal shifts.", "Legacy, reception, and cultural impact."]')
        if 'Return a strict JSON array of strings' in prompt:
            return self._Resp('["Introduction and premise.", "Foundational context.", "Deep thematic analysis.", "Counterpoints and complexities.", "Implications and conclusion."]')
        # drafting section
        return self._Resp("This is a mock drafted section used in offline mode. It simulates generated prose so you can test the pipeline without a network call.")

def _configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scribe Agent - Video Essay Script Generator")
    parser.add_argument("--check", action="store_true", help="Run a quick model health check and exit")
    parser.add_argument("--topic", type=str, default=None, help="Provide a topic to skip the prompt")
    parser.add_argument("--theme-index", type=int, default=None, help="Choose a theme by index (1-based) to skip selection")
    parser.add_argument("--sections", type=int, default=None, help="Number of outline sections (1-12)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--offline", action="store_true", help="Run without real API calls (mock outputs)")
    return parser.parse_args(argv)


def _health_check() -> int:
    try:
        logging.info("Setting up model for health check…")
        model = setup_model()
        resp = model.generate_content("ping")
        ok = bool(resp and getattr(resp, "text", "").strip())  # direct .text access expected in current lib
        print("OK" if ok else "FAILED")
        return 0 if ok else 2
    except KeyboardInterrupt:
        print("Cancelled")
        return 130
    except Exception as e:
        logging.debug("Health check error", exc_info=True)
        print(f"Health check failed: {e}")
        return 1


def _prompt_int(prompt: str, default: int | None = None, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            val = int(raw)
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Please enter a number between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    _configure_logging(args.verbose)

    print("🎬 Welcome to Scribe Agent - Video Essay Script Generator")
    print("=" * 60)

    if args.check:
        return _health_check()

    try:
        if args.offline:
            logging.info("Using offline mock model (no API calls).")
            model = OfflineMockModel()
        else:
            logging.info("Setting up model…")
            model = setup_model()

        # Topic input
        topic = (args.topic or input("\n📝 Enter your video essay topic: ").strip())
        if not topic:
            print("❌ No topic provided. Exiting.")
            return 2

        logging.info("Brainstorming themes…")
        themes = brainstorm_themes(topic, model)
        if not themes:
            print("❌ Could not generate themes. Check your API key, network, and try again.")
            return 3

        print(f"\n🎯 Generated themes for '{topic}':")
        for i, theme in enumerate(themes, 1):
            print(f"{i}. {theme}")

        # Theme selection
        if args.theme_index is not None:
            choice = args.theme_index
            if not (1 <= choice <= len(themes)):
                print(f"❌ theme-index must be between 1 and {len(themes)}")
                return 4
        else:
            choice = _prompt_int(f"\nChoose a theme (1-{len(themes)}): ", min_val=1, max_val=len(themes))

        chosen_theme = themes[choice - 1]
        print(f"\n✅ Selected theme: {chosen_theme}")

        # Outline sections
        num_sections = args.sections if args.sections is not None else _prompt_int("\nHow many sections should the outline have? (default: 8): ", default=8, min_val=1, max_val=12)

        logging.info("Generating outline…")
        outline = create_outline(topic, chosen_theme, model, num_sections)
        if not outline:
            print("❌ Could not generate outline. Try a simpler topic or fewer sections.")
            return 5

        print(f"\n📋 Generated outline:")
        for i, section in enumerate(outline, 1):
            print(f"{i}. {section}")

        # Confirm
        if args.topic is None or args.theme_index is None or args.sections is None:
            proceed = input("\nProceed with drafting the full script? (y/N): ").strip().lower()
            if proceed != 'y':
                print("Script generation cancelled.")
                return 0

        print(f"\n🖊️  Starting script drafting…")
        full_script = ""

        for i, section_outline in enumerate(outline, 1):
            print(f"\n--- Section {i}/{len(outline)} ---")
            logging.info("Drafting section %s/%s", i, len(outline))
            section_text = draft_section(
                topic=topic,
                theme=chosen_theme,
                outline_point=section_outline,
                previous_sections=full_script,
                model=model
            )

            if section_text:
                full_script += f"\n\n{section_text}"
                print(f"✅ Section {i} completed ({len(section_text.split())} words)")
            else:
                print(f"⚠️  Section {i} failed - continuing with next section")

        if full_script.strip():
            filename = save_script(topic, chosen_theme, outline, full_script)
            if filename:
                print(f"\n🎉 Script generation complete!")
                print(f"📁 Saved to: {filename}")
                print(f"📊 Total words: {len(full_script.split())}")
                return 0
            else:
                print("❌ Failed to save the script to disk.")
                return 6
        else:
            print("❌ No script content was generated.")
            return 7

    except KeyboardInterrupt:
        print("\n\n⏹️  Script generation cancelled by user.")
        return 130
    except ValueError as e:
        logging.debug("ValueError in main", exc_info=True)
        print(f"\n❌ Configuration error: {e}")
        return 10
    except Exception as e:
        logging.debug("Unhandled error in main", exc_info=True)
        print(f"\n❌ An unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
