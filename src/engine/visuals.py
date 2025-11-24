from playwright.sync_api import sync_playwright
import time
import os

class VisualEngine:
    def __init__(self, headless=True):
        self.headless = headless

    def record_repo_tour(self, repo_url, output_path="output/video.mp4"):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                record_video_dir=os.path.dirname(output_path),
                record_video_size={"width": 1920, "height": 1080},
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()

            # Navigate to Repo
            page.goto(repo_url)
            page.wait_for_load_state("networkidle")

            # Simulate reading (scroll down)
            for _ in range(5):
                page.mouse.wheel(0, 500)
                time.sleep(2)

            # Click on Issues or Pull Requests to show activity
            # (This is a basic example, can be made smarter)
            try:
                page.click("a[id='issues-tab']", timeout=2000)
                time.sleep(2)
            except:
                pass

            context.close()
            browser.close()

            # Rename the video file (Playwright saves with random name)
            # Find the latest video in the dir and rename it

            # Playwright saves the video file after context close.
            # We need to find the file created in the directory.
            # Since we set record_video_dir to os.path.dirname(output_path), we look there.

            output_dir = os.path.dirname(output_path)
            # List files in output dir
            files = [f for f in os.listdir(output_dir) if f.endswith(".webm")]
            # Sort by modification time
            files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)))

            if files:
                latest_video = files[-1]
                source = os.path.join(output_dir, latest_video)

                # Playwright records in WebM.
                # If the requested output_path is .mp4, we should ideally convert it.
                # However, MoviePy (used in Renderer) can read WebM fine.
                # To avoid "corrupt" files (WebM content in MP4 container), we force .webm extension here.
                # The Renderer will handle the final conversion to MP4.

                base, _ = os.path.splitext(output_path)
                final_path = f"{base}.webm"

                if os.path.exists(final_path):
                    os.remove(final_path)

                os.rename(source, final_path)
                return final_path
            return None
