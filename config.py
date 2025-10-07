import os
from pathlib import Path
from typing import Optional, Tuple
from dotenv import load_dotenv
import google.generativeai as genai

FALLBACK_KEY_VARS = [
    "GOOGLE_API_KEY",
    "GOOGLE_API_KEY_2",
    "GEMINI_API_KEY",
    "GEMINI_API_KEY_2",
]


def _find_api_key() -> Optional[Tuple[str, str]]:
    """Return (key, var_name) for the first matching env var, else None."""
    for name in FALLBACK_KEY_VARS:
        val = os.getenv(name)
        if val:
            return val, name
    return None


def setup_model(model_name: str = 'gemini-1.5-flash'):
    """Configure and return a GenerativeModel.

    Looks for an API key in multiple environment variable names to
    accommodate user variations. Loads a local .env if present.
    """
    # Load environment variables from a .env file if present
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    found = _find_api_key()
    if not found:
        print("❌ Error: No API key found.")
        print("Checked variables: " + ", ".join(FALLBACK_KEY_VARS))
        print("Set one in .env, e.g.: GOOGLE_API_KEY=your-ai-studio-key")
        raise ValueError("Google API key not found")
    api_key, var_name = found

    # Configure the API (do not log full key)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    masked = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "(hidden)"
    print(f"✅ Google Generative AI model configured successfully (key var: {var_name}, value: {masked}).")
    return model
