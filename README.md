# Scribe Agent - Video Essay Script Generator

🎬 **An AI-powered tool for generating long-form video essay scripts using Google's Gemini AI.**

Generate compelling, personal video essay scripts on any topic with structured outlines, thematic analysis, and first-person narrative style.

## ✨ Features

- **Interactive Topic Selection**: Enter any topic and get 5 AI-generated themes to choose from
- **Customizable Structure**: Choose the number of sections (4-8 recommended)
- **Personal Perspective**: Scripts written in first-person with personal insights and reflections
- **Professional Output**: Complete scripts with outlines, themes, and word counts
- **Timestamped Files**: Automatically saves scripts with timestamps for organization

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/scribe-agent.git
   cd scribe-agent
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   source .venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API key:**
   ```bash
   # Windows PowerShell
   $env:GOOGLE_API_KEY="your-api-key-here"
   
   # macOS/Linux
   export GOOGLE_API_KEY="your-api-key-here"
   ```

### Usage

```bash
python main.py
```

Follow the interactive prompts:
1. Enter your video essay topic
2. Choose from 5 generated themes  
3. Set number of sections (default: 8)
4. Confirm and let the AI generate your script

## 📁 Project Structure

```
scribe-agent/
├── main.py              # Main script runner
├── config.py            # API configuration
├── requirements.txt     # Python dependencies
├── modules/
│   ├── brainstormer.py  # Theme generation
│   ├── outliner.py      # Outline creation
│   ├── drafter.py       # Script drafting
│   └── file_manager.py  # File operations
└── outputs/             # Generated scripts (gitignored)
```

## 🎯 Example Topics

- "The Philosophy of The Matrix"
- "Why Avatar: The Last Airbender is Perfect"
- "The Rise and Fall of Blockbuster Video"
- "Political Themes in Dune Messiah"
- "The Evolution of Marvel Storytelling"

## ⚙️ Configuration

### Script Length
- **4 sections**: ~6,000 words (more concise, less repetitive)
- **8 sections**: ~6,000-6,500 words (detailed analysis)

### Writing Style
Scripts are generated with:
- First-person perspective ("I find fascinating...", "What strikes me...")
- Personal reflections and analysis
- Sophisticated but accessible language
- Natural transitions between sections

## 🔧 Customization

### Modify Writing Style
Edit the prompt in `modules/drafter.py` to adjust:
- Tone and voice
- Perspective (first/third person)  
- Complexity level
- Target audience

### Change AI Model
Update `config.py` to use different Gemini models:
- `gemini-1.5-flash` (current, fast)
- `gemini-1.5-pro` (more sophisticated)

## 📊 Output Format

Generated scripts include:
- **Header**: Topic, theme, generation timestamp
- **Outline**: Numbered section breakdown
- **Script**: Complete essay text with word counts
- **Filename**: `script_[topic]_[timestamp].txt`

## 🚫 What's Not Included

- API keys (you provide your own)
- Generated scripts (saved locally only)
- Virtual environment files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## ⚠️ Important Notes

- **API Costs**: Each script generation uses ~10-15 API calls
- **Runtime**: 1-3 minutes per complete script
- **Cancellation**: Press `Ctrl+C` to cancel at any time
- **Privacy**: Your API key stays local, scripts aren't uploaded anywhere

## 🆘 Troubleshooting

### "API key not found"
Make sure you've set the `GOOGLE_API_KEY` environment variable.

### "Model not found" 
Update the model name in `config.py` if Google changes their API.

### Long topic names
The script automatically truncates long filenames to avoid Windows path limits.

---

**Happy script writing!** 🎬✨
