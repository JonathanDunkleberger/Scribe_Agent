import os
from datetime import datetime

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
    # Create outputs directory if it doesn't exist
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_topic = safe_topic.replace(' ', '_')
    
    # Limit the topic length to avoid Windows file path limits
    max_topic_length = 50
    if len(safe_topic) > max_topic_length:
        safe_topic = safe_topic[:max_topic_length]
    
    filename = f"{output_dir}/script_{safe_topic}_{timestamp}.txt"
    
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
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Script saved to: {filename}")
        return filename
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
