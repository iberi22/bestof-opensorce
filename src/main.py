import argparse
import os
import logging
import time
import asyncio
from dotenv import load_dotenv
from scanner.github_scanner import GitHubScanner
from agents.scriptwriter import ScriptWriter
from engine.visuals import VisualEngine
from engine.renderer import ContentRenderer
from uploader.youtube import YouTubeUploader
from persistence.firebase_store import FirebaseStore
from image_gen.image_generator import ImageGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Open Source Video Generator")
    parser.add_argument("--mode", choices=["once", "daemon"], default="once", help="Run once or as a daemon")
    parser.add_argument("--provider", choices=["gemini", "foundry"], default="gemini", help="LLM Provider")
    parser.add_argument("--model", default="gemini-1.5-flash", help="Model name (e.g., gemini-1.5-flash or phi-3.5-mini)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--use-firebase", action="store_true", help="Enable Firebase persistence")
    parser.add_argument("--generate-images", action="store_true", help="Generate explanatory images with Nano Banana 2")

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

    # Firebase Persistence (Optional)
    firebase_store = None
    if args.use_firebase:
        try:
            firebase_store = FirebaseStore()
            logging.info("Firebase persistence enabled")
        except Exception as e:
            logging.warning(f"Failed to initialize Firebase: {e}. Continuing without persistence.")

    # Image Generator (Optional)
    image_generator = None
    if args.generate_images:
        try:
            image_generator = ImageGenerator(model_name="nano-banana-2")
            logging.info("Image generation enabled with Nano Banana 2")
        except Exception as e:
            logging.warning(f"Failed to initialize ImageGenerator: {e}. Continuing without images.")

    def job():
        logging.info("Starting scan job...")
        repos = scanner.scan_recent_repos(limit=5)
        logging.info(f"Found {len(repos)} potential repos.")

        for repo in repos:
            repo_full_name = repo['full_name']

            # Check if already processed (if Firebase enabled)
            if firebase_store and firebase_store.is_processed(repo_full_name):
                logging.info(f"Skipping {repo_full_name} - already processed")
                continue

            if scanner.validate_repo(repo):
                logging.info(f"Processing repo: {repo_full_name}")

                # Save to Firebase as "pending" (if enabled)
                if firebase_store:
                    firebase_store.save_repo(repo_full_name, repo, status="pending")

                try:
                    # Update status to "processing"
                    if firebase_store:
                        firebase_store.update_status(repo_full_name, status="processing")

                    # 1. Generate Script
                    script = scriptwriter.generate_script(repo)
                    if not script:
                        logging.warning("Failed to generate script. Skipping.")
                        if firebase_store:
                            firebase_store.update_status(
                                repo_full_name,
                                status="failed",
                                error_message="Script generation failed"
                            )
                        continue

                    logging.info(f"Script generated: {script.get('hook')}")

                    # 1.5. Generate Images (Optional)
                    if image_generator:
                        logging.info("Generating explanatory images...")
                        try:
                            # Generate architecture diagram
                            arch_img = image_generator.generate_architecture_diagram(repo, script)
                            if arch_img:
                                logging.info(f"Architecture diagram: {arch_img}")

                            # Generate problem-solution flow
                            flow_img = image_generator.generate_problem_solution_flow(repo, script)
                            if flow_img:
                                logging.info(f"Flow diagram: {flow_img}")

                            # Generate feature showcase if pros available
                            if script.get('pros'):
                                feature_img = image_generator.generate_feature_showcase(repo, script['pros'])
                                if feature_img:
                                    logging.info(f"Feature showcase: {feature_img}")
                        except Exception as e:
                            logging.warning(f"Image generation failed: {e}")

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
                    # video_url = uploader.upload_video(
                    #     final_video_path,
                    #     title=f"{repo['name']} - {script['hook']}",
                    #     description=script['narration']
                    # )

                    # Mark as completed
                    if firebase_store:
                        firebase_store.update_status(
                            repo_full_name,
                            status="completed",
                            # video_url=video_url  # Uncomment when upload is enabled
                        )

                    logging.info(f"Finished processing {repo_full_name}")

                except Exception as e:
                    logging.error(f"Error processing {repo_full_name}: {e}")
                    if firebase_store:
                        firebase_store.update_status(
                            repo_full_name,
                            status="failed",
                            error_message=str(e)
                        )

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
