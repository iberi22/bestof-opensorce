"""
Test script for Reel Creator.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_generator.reel_creator import ReelCreator

def test_reel_creation():
    print("\n🎬 Testing ReelCreator...")

    # Mock data
    repo_name = "test-reel-project"

    script_data = {
        "hook": "Manual deployments are killing your productivity",
        "solution": "Automate everything with this simple tool",
    }

    # Ensure dummy images exist in tests output directory (not in blog assets)
    img_dir = Path(__file__).parent / "output" / "test-images"
    img_dir.mkdir(parents=True, exist_ok=True)

    # Create dummy images using PIL if they don't exist
    from PIL import Image, ImageDraw

    def create_dummy_img(name, color):
        path = img_dir / f"{name}.png"
        if not path.exists():
            img = Image.new('RGB', (800, 600), color=color)
            d = ImageDraw.Draw(img)
            d.text((10,10), name, fill=(255,255,255))
            img.save(path)
        return str(path)

    images = {
        "architecture": create_dummy_img("architecture", "blue"),
        "flow": create_dummy_img("flow", "green"),
        "screenshot": create_dummy_img("screenshot", "red")
    }

    try:
        output_dir = Path(__file__).parent / "output_videos"
        output_dir.mkdir(parents=True, exist_ok=True)
        creator = ReelCreator(output_dir=str(output_dir))
        print("✅ ReelCreator initialized")

        output_path = creator.create_reel(
            repo_name=repo_name,
            script_data=script_data,
            images=images
        )

        if output_path and os.path.exists(output_path):
            print(f"✅ Reel created successfully: {output_path}")
            return True
        else:
            print("❌ Failed to create reel (no output file)")
            return False

    except Exception as e:
        print(f"❌ Reel creation failed: {e}")
        return False

if __name__ == "__main__":
    test_reel_creation()
