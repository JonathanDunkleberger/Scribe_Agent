import google.generativeai as genai
import ast

def brainstorm_themes(topic: str, model: genai.GenerativeModel) -> list[str]:
    """
    Generates a list of potential themes for a video essay on a given topic.

    Args:
        topic (str): The high-level topic (e.g., "The Dune Novels").
        model (genai.GenerativeModel): The initialized generative model.

    Returns:
        list[str]: A list of 5 potential themes.
    """
    print(f"\n🧠 Brainstorming themes for: {topic}...")

    prompt = f"""
    I am creating a long-form video essay on the topic of "{topic}".
    Please brainstorm a list of 5 distinct and compelling themes or core arguments that could serve as the foundation for the entire essay.
    Each theme should be a concise, single sentence.

    Example for the topic "Star Wars":
    - The cyclical nature of war and rebellion across generations.
    - The conflict between technological advancement and spiritual faith (The Force).
    - How the Skywalker family saga serves as a modern mythological epic.
    - An analysis of the political decay from a Republic to an Empire.
    - The theme of redemption and the possibility of change even for the most evil.

    Now, generate 5 themes for the topic: "{topic}".
    Return the themes as a Python list of strings. For example: ["Theme 1.", "Theme 2.", "Theme 3.", "Theme 4.", "Theme 5."]
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Handle cases where the response is wrapped in code blocks
        if response_text.startswith("```python"):
            # Extract the list from between the code blocks
            lines = response_text.split('\n')
            code_lines = []
            in_code_block = False
            for line in lines:
                if line.startswith("```python"):
                    in_code_block = True
                elif line.startswith("```"):
                    in_code_block = False
                elif in_code_block and not line.startswith("print("):
                    code_lines.append(line)
            
            # Join the code lines and evaluate
            code_text = '\n'.join(code_lines)
            local_vars = {}
            exec(code_text, {}, local_vars)
            themes = local_vars.get('themes', [])
        else:
            # Try to parse as direct list
            themes = ast.literal_eval(response_text)
        
        print("✅ Brainstorming complete.")
        return themes
    except (ValueError, SyntaxError) as e:
        print(f"❌ Error parsing themes from model response: {e}")
        print(f"Raw response was: {response.text}")
        return []
    except Exception as e:
        print(f"❌ An unexpected error occurred during brainstorming: {e}")
        return []

