import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

def setup_model():
    """
    Sets up the Google Generative AI model.
    
    Returns:
        genai.GenerativeModel: The configured model instance.
    """
    # Load environment variables from a .env file if present
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found.")
        print("Set it in one of these ways:")
        print("1) Create a .env file next to config.py with: GOOGLE_API_KEY=your-api-key-here")
        print("2) Set in current PowerShell session: $env:GOOGLE_API_KEY='your-api-key-here'")
        print("3) Persist for your user: [Environment]::SetEnvironmentVariable('GOOGLE_API_KEY','your-api-key-here','User')")
        raise ValueError("Google API key not found")
    
    # Configure the API
    genai.configure(api_key=api_key)
    
    # Create and return the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Google Generative AI model configured successfully.")
    return model
