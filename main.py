#!/usr/bin/env python3
"""
Scribe Agent - Video Essay Script Generator

A tool for generating long-form video essay scripts using AI.
Generates compelling, personal video essays with structured outlines
and first-person narrative style.

Usage:
    python main.py

Requirements:
    - Google AI API key set as GOOGLE_API_KEY environment variable
    - Internet connection for API calls

Author: Scribe Agent
Version: 1.0.0
"""

from config import setup_model
from modules.brainstormer import brainstorm_themes
from modules.outliner import create_outline
from modules.drafter import draft_section
from modules.file_manager import save_script

def main():
    """Main execution function for the script generator."""
    print("🎬 Welcome to Scribe Agent - Video Essay Script Generator")
    print("=" * 60)
    
    try:
        # Setup the AI model
        model = setup_model()
        
        # Get topic from user
        topic = input("\n📝 Enter your video essay topic: ").strip()
        if not topic:
            print("❌ No topic provided. Exiting.")
            return
        
        # Brainstorm themes
        themes = brainstorm_themes(topic, model)
        if not themes:
            print("❌ Could not generate themes. Exiting.")
            return
        
        # Display themes and let user choose
        print(f"\n🎯 Generated themes for '{topic}':")
        for i, theme in enumerate(themes, 1):
            print(f"{i}. {theme}")
        
        while True:
            try:
                choice = int(input(f"\nChoose a theme (1-{len(themes)}): "))
                if 1 <= choice <= len(themes):
                    chosen_theme = themes[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(themes)}")
            except ValueError:
                print("Please enter a valid number")
        
        print(f"\n✅ Selected theme: {chosen_theme}")
        
        # Create outline
        num_sections = int(input("\nHow many sections should the outline have? (default: 8): ") or "8")
        outline = create_outline(topic, chosen_theme, model, num_sections)
        
        if not outline:
            print("❌ Could not generate outline. Exiting.")
            return
        
        # Display outline
        print(f"\n📋 Generated outline:")
        for i, section in enumerate(outline, 1):
            print(f"{i}. {section}")
        
        # Confirm before drafting
        proceed = input("\nProceed with drafting the full script? (y/N): ").strip().lower()
        if proceed != 'y':
            print("Script generation cancelled.")
            return
        
        # Draft each section
        print(f"\n🖊️  Starting script drafting...")
        full_script = ""
        
        for i, section_outline in enumerate(outline, 1):
            print(f"\n--- Section {i}/{len(outline)} ---")
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
        
        # Save the script
        if full_script.strip():
            filename = save_script(topic, chosen_theme, outline, full_script)
            
            print(f"\n🎉 Script generation complete!")
            print(f"📁 Saved to: {filename}")
            print(f"📊 Total words: {len(full_script.split())}")
        else:
            print("❌ No script content was generated.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Script generation cancelled by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
