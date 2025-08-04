import os
import google.generativeai as genai

def setup_model():
    """
    Sets up the Google Generative AI model.
    
    Returns:
        genai.GenerativeModel: The configured model instance.
    """
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set your Google API key:")
        print("$env:GOOGLE_API_KEY='your-api-key-here'")
        raise ValueError("Google API key not found")
    
    # Configure the API
    genai.configure(api_key=api_key)
    
    # Create and return the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Google Generative AI model configured successfully.")
    return model
