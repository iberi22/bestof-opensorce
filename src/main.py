import argparse
import os
import logging
import time
import asyncio
from dotenv import load_dotenv
from src.scanner.github_scanner import GitHubScanner
from src.agents.scriptwriter import ScriptWriter
from src.engine.visuals import VisualEngine
from src.engine.renderer import ContentRenderer
from src.uploader.youtube import YouTubeUploader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Open Source Video Generator")
    parser.add_argument("--mode", choices=["once", "daemon"], default="once", help="Run once or as a daemon")
    parser.add_argument("--provider", choices=["gemini", "foundry"], default="gemini", help="LLM Provider")
    parser.add_argument("--model", default="gemini-1.5-flash", help="Model name (e.g., gemini-1.5-flash or phi-3.5-mini)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")

    args = parser.parse_args()

    load_dotenv()

    # Validate Environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logging.error("GITHUB_TOKEN is missing")
        return

    # Initialize Components
    scanner = GitHubScanner(token=github_token)

    api_key = os.getenv("GOOGLE_API_KEY") if args.provider == "gemini" else None
    try:
        scriptwriter = ScriptWriter(api_key=api_key, provider=args.provider, model_name=args.model)
    except Exception as e:
        logging.error(f"Failed to initialize ScriptWriter: {e}")
        return

    visual_engine = VisualEngine(headless=args.headless)
    renderer = ContentRenderer()

    # Uploader (Mock for now)
    uploader = YouTubeUploader(
        client_secret_file=os.getenv("YOUTUBE_CLIENT_SECRET"),
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN")
    )

    def job():
        logging.info("Starting scan job...")
        repos = scanner.scan_recent_repos(limit=5)
        logging.info(f"Found {len(repos)} potential repos.")

        for repo in repos:
            if scanner.validate_repo(repo):
                logging.info(f"Processing repo: {repo['full_name']}")

                # 1. Generate Script
                script = scriptwriter.generate_script(repo)
                if not script:
                    logging.warning("Failed to generate script. Skipping.")
                    continue

                logging.info(f"Script generated: {script.get('hook')}")

                # 2. Record Video (Visuals)
                raw_video_path = f"output/{repo['name']}_raw.mp4"
                visual_engine.record_repo_tour(repo['html_url'], output_path=raw_video_path)

                # 3. Render Video (Audio + Editing)
                audio_path = f"output/{repo['name']}.mp3"
                final_video_path = f"output/{repo['name']}_final.mp4"

                logging.info("Generating narration...")
                asyncio.run(renderer.generate_audio(script.get('narration', 'No narration provided.'), output_file=audio_path))

                logging.info("Composing final video...")
                renderer.compose_video(raw_video_path, audio_path, final_video_path)

                # 4. Upload
                # uploader.upload_video(final_video_path, title=f"{repo['name']} - {script['hook']}", description=script['narration'])

                logging.info(f"Finished processing {repo['full_name']}")

                # Break after one successful video for testing
                break

    if args.mode == "once":
        job()
    elif args.mode == "daemon":
        logging.info("Running in daemon mode (scanning every hour)...")
        while True:
            job()
            time.sleep(3600) # 1 hour

if __name__ == "__main__":
    main()
