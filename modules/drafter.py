import google.generativeai as genai

def draft_section(
    topic: str,
    theme: str,
    outline_point: str,
    previous_sections: str,
    model: genai.GenerativeModel,
    word_count: int = 750
) -> str:
    """
    Drafts a single section of the video essay script.

    Args:
        topic (str): The high-level topic.
        theme (str): The core theme of the essay.
        outline_point (str): The specific point from the outline this section should cover.
        previous_sections (str): The concatenated text of all previously written sections.
        model (genai.GenerativeModel): The initialized generative model.
        word_count (int): The target word count for this section.

    Returns:
        str: The drafted script for the section.
    """
    print(f"\n✍️ Drafting section: '{outline_point}'...")

    # For the very first section, the context is different.
    if not previous_sections:
        context_prompt = f"This is the very first section of the script. It should serve as a powerful introduction to the entire video essay."
    else:
        context_prompt = f"""
        Here is the script that has been written so far, for context.
        Do NOT repeat information from this context unless it is absolutely necessary for transition.
        --- CONTEXT START ---
        {previous_sections}
        --- CONTEXT END ---
        """

    prompt = f"""
    You are a thoughtful and reflective writer, creating a script for my personal YouTube video essay. 
    Write from a first-person perspective, using "I". I want you to explore my personal feelings, thoughts, and interpretations of the material. 
    For example, use phrases like "I was struck by...", "What I find fascinating is...", or "It feels to me as though...".
    
    The overall topic is "{topic}".
    The central theme is "{theme}".

    {context_prompt}

    Your current task is to write the next section of the script. This section must focus *exclusively* on the following point from our outline:
    **"{outline_point}"**

    Write this section in an engaging, personal, and sophisticated style from my perspective. It should be approximately {word_count} words long.
    Do not write a title or a heading like "Section 2". Just write the body of the script for this section.
    Ensure a smooth, natural transition from the previous content into this new section.
    Make it feel like my personal reflection and analysis, not a generic academic essay.
    """

    try:
        response = model.generate_content(prompt)
        print("✅ Section drafted.")
        return response.text
    except Exception as e:
        print(f"❌ An unexpected error occurred during drafting: {e}")
        return ""
