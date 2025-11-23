# Open Source Video Generator

Automated tool to scan GitHub for trending repositories, generate a video script using AI (Gemini or Foundry Local), record a visual tour, and narrate it.

## Features

- **GitHub Scanner**: Finds recent, high-quality repositories (CI passing, good description).
- **AI Scriptwriter**: Generates engaging scripts using Google Gemini or Microsoft Foundry Local (for local LLMs).
- **Visual Engine**: Records a browser tour of the repository using Playwright.
- **Content Renderer**: Generates professional narration using Edge TTS and combines it with the video.
- **YouTube Uploader**: (Mock) Uploads the final video.

## Prerequisites

- Python 3.10+
- FFmpeg (for MoviePy)
- Google API Key (if using Gemini)
- Foundry Local (if using local LLMs)

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. Create a `.env` file based on `.env.example`.

## Usage

### Run Once (Default)
```bash
python src/main.py --mode once
```

### Run as Daemon (Hourly Scan)
```bash
python src/main.py --mode daemon
```

### Use Local LLM (Foundry Local)
Ensure Foundry Local is running or installed.
```bash
python src/main.py --provider foundry --model phi-3.5-mini
```

### Headless Mode (for Server/CI)
```bash
python src/main.py --headless
```

## Architecture

- `src/scanner`: GitHub API interaction.
- `src/agents`: LLM interaction (Gemini/Foundry).
- `src/engine`: Visual recording (Playwright) and Rendering (MoviePy + EdgeTTS).
- `src/uploader`: YouTube API interaction.