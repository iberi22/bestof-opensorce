# Implementation Summary

## Project Overview
This project automates the creation of videos for Open Source GitHub repositories. It scans for trending repos, generates a script using AI, records a visual tour, and narrates it.

## Key Features Implemented
1.  **Hybrid Architecture**: Supports both Cloud (Gemini) and Local (Foundry Local) LLMs.
2.  **GitHub Scanner**: Filters repositories based on quality (CI status, description).
3.  **Visual Engine**: Uses Playwright to record a browser tour of the repository.
4.  **Content Renderer**: Uses Edge TTS for narration and MoviePy for video composition.
5.  **Docker Support**: Includes Dockerfile and docker-compose.yml.

## How to Use Foundry Local (Local LLM)
To use local models and save costs:
1.  Install [Foundry Local](https://github.com/microsoft/Foundry-Local).
2.  Run the script with the `--provider foundry` flag.
    ```bash
    python -m src.main --provider foundry --model phi-3.5-mini
    ```
    *Note: Ensure the model alias (e.g., `phi-3.5-mini`) is available in your Foundry Local setup.*

## Next Steps
-   **YouTube Upload**: The `src/uploader/youtube.py` is currently a mock. You need to implement the actual OAuth2 logic using `google-auth-oauthlib`.
-   **Enhanced Visuals**: Improve `VisualEngine` to highlight specific elements mentioned in the script.
-   **Video Editing**: Improve `ContentRenderer` to sync audio with specific video segments.

## Files
-   `src/main.py`: Entry point.
-   `src/agents/scriptwriter.py`: Handles Gemini and Foundry logic.
-   `src/engine/`: Contains Visuals and Renderer.
-   `src/scanner/`: GitHub scanning logic.
