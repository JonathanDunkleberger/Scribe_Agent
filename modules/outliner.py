import google.generativeai as genai
import ast

def create_outline(topic: str, theme: str, model: genai.GenerativeModel, sections: int = 8) -> list[str]:
    """
    Creates a detailed outline for the video essay based on the chosen theme.

    Args:
        topic (str): The high-level topic.
        theme (str): The chosen core theme for the essay.
        model (genai.GenerativeModel): The initialized generative model.
        sections (int): The number of sections the outline should have.

    Returns:
        list[str]: A list of strings, where each string is a section title/description.
    """
    print(f"\n📝 Creating a {sections}-part outline for the theme: '{theme}'...")

    prompt = f"""
    I am creating a long-form video essay about "{topic}", focusing on the theme: "{theme}".
    Create a detailed, {sections}-part outline for the entire script.
    Each part of the outline should be a single, descriptive sentence that clearly states what that section of the video will cover.
    The outline should have a logical flow, starting with an introduction, developing the argument through the body, and ending with a conclusion.

    Example for the theme "The Dangers of the Messianic Hero in Dune":
    [
        "Introduction: Introduce the concept of the messianic archetype and pose the central question of Paul Atreides' heroism.",
        "The Bene Gesserit's Plan: Detail the Missionaria Protectiva and the centuries of religious engineering that paved Paul's path.",
        "The Weight of Terrible Purpose: Analyze Paul's prescience, exploring how seeing the future trapped him and forced his hand into jihad.",
        "The Fremen's Holy War: Describe the explosion of violence and fanaticism once Paul accepts his role as the Lisan al Gaib.",
        "The Golden Path's Shadow: Discuss the initial motivations behind the Golden Path and its horrific long-term cost to humanity.",
        "The Tyrant's Legacy in Dune Messiah: Show the horrific fallout of Paul's reign and how he ultimately failed to stop the machine he created.",
        "The Failure of the Hero: Argue that Paul's ultimate tragedy was his inability to escape the very myth he embodied.",
        "Conclusion: Summarize Herbert's warning about charismatic leaders and the dangers of placing faith in a single savior."
    ]

    Now, generate a {sections}-part outline for the topic "{topic}" with the theme "{theme}".
    Return the outline *only* as a Python list of strings.
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Handle cases where the response is wrapped in code blocks
        if response_text.startswith("```python"):
            # Extract the list from between the code blocks
            lines = response_text.split('\n')
            list_lines = []
            in_code_block = False
            for line in lines:
                if line.startswith("```python"):
                    in_code_block = True
                elif line.startswith("```"):
                    in_code_block = False
                elif in_code_block and (line.startswith("[") or line.startswith('"') or line.startswith("]") or line.strip().startswith('"')):
                    list_lines.append(line)
            
            # Join the list lines and evaluate
            list_text = '\n'.join(list_lines)
            outline = ast.literal_eval(list_text)
        else:
            # Try to parse as direct list
            outline = ast.literal_eval(response_text)
        
        if isinstance(outline, list) and all(isinstance(item, str) for item in outline):
            print("✅ Outline created successfully.")
            return outline
        else:
            raise ValueError("Model did not return a valid list of strings.")
    except (ValueError, SyntaxError) as e:
        print(f"❌ Error parsing outline from model response: {e}")
        print(f"Raw response was: {response.text}")
        return []
    except Exception as e:
        print(f"❌ An unexpected error occurred during outlining: {e}")
        return []
