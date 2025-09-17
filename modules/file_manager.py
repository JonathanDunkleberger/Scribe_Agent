from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

def save_script(topic: str, theme: str, sections: list[str], script_text: str) -> str:
    """
    Saves the completed script to a file.
    
    Args:
        topic (str): The video essay topic
        theme (str): The chosen theme
        sections (list[str]): The outline sections
        script_text (str): The complete script text
        
    Returns:
        str: The filename where the script was saved
    """
    # Ensure outputs directory
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = re.sub(r"[^A-Za-z0-9\-_ ]+", "", topic).strip()
    safe_topic = re.sub(r"\s+", "_", base)
    
    # Limit the topic length to avoid Windows file path limits
    max_topic_length = 50
    if len(safe_topic) > max_topic_length:
        safe_topic = safe_topic[:max_topic_length]
    
    filename = output_dir / f"script_{safe_topic}_{timestamp}.txt"
    
    # Create the content
    content = f"""VIDEO ESSAY SCRIPT
Topic: {topic}
Theme: {theme}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OUTLINE:
{chr(10).join(f"{i+1}. {section}" for i, section in enumerate(sections))}

SCRIPT:
{script_text}
"""
    
    # Save to file
    try:
        filename.write_text(content, encoding='utf-8')
        print(f"✅ Script saved to: {filename}")
        return str(filename)
    except Exception as e:
        print(f"❌ Error saving script: {e}")
        return ""

def load_script(filename: str) -> str:
    """
    Loads a script from a file.
    
    Args:
        filename (str): The filename to load
        
    Returns:
        str: The script content
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error loading script: {e}")
        return ""
