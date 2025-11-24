"""
Demo script for multilingual reel generation.

This demonstrates the complete workflow:
1. Record/provide reference voice
2. Write script
3. Generate audio in multiple languages
4. Create video reels
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_generator.voice_cloning import MultilingualReelGenerator
from video_generator.reel_creator import ReelCreator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demo_multilingual_generation():
    """
    Demo: Generate reels in multiple languages.
    """

    # Configuration
    REFERENCE_AUDIO = "path/to/your/reference_voice.wav"  # Your voice sample
    REPO_NAME = "awesome-open-source-project"

    # Script (20 seconds, ~50 words)
    SCRIPT = """
    Discover this amazing open source project that solves a common developer problem.
    It provides a clean API, excellent documentation, and active community support.
    Perfect for modern web applications. Check out the link in the description!
    """

    # Target languages
    TARGET_LANGUAGES = ["en", "es", "fr", "de", "pt"]

    logger.info("=" * 60)
    logger.info("🎬 Multilingual Reel Generation Demo")
    logger.info("=" * 60)

    # Step 1: Generate multilingual audio
    logger.info("\n📢 Step 1: Generating audio in multiple languages...")
    logger.info(f"Target languages: {', '.join(TARGET_LANGUAGES)}")

    generator = MultilingualReelGenerator(
        reference_audio=REFERENCE_AUDIO,
        output_dir="output/audio/multilingual"
    )

    audio_files = generator.generate_multilingual_audio(
        script=SCRIPT,
        repo_name=REPO_NAME,
        target_languages=TARGET_LANGUAGES
    )

    if not audio_files:
        logger.error("❌ Failed to generate audio files")
        return

    logger.info(f"✅ Generated {len(audio_files)} audio files:")
    for lang, path in audio_files.items():
        logger.info(f"  - {lang}: {path}")

    # Step 2: Generate video reels
    logger.info("\n🎥 Step 2: Creating video reels...")

    reel_creator = ReelCreator(output_dir="output/videos")

    # Placeholder images (in production, these come from blog post)
    images = {
        'architecture': 'blog/assets/images/placeholder/architecture.png',
        'flow': 'blog/assets/images/placeholder/flow.png',
        'screenshot': 'blog/assets/images/placeholder/screenshot.png'
    }

    script_data = {
        'hook': SCRIPT[:100],
        'solution': SCRIPT,
        'verdict': 'Check it out!'
    }

    video_files = {}

    for lang, audio_path in audio_files.items():
        logger.info(f"  Creating reel for {lang.upper()}...")

        video_path = reel_creator.create_reel(
            repo_name=f"{REPO_NAME}-{lang}",
            script_data=script_data,
            images=images,
            audio_path=audio_path
        )

        if video_path:
            video_files[lang] = video_path
            logger.info(f"  ✅ {lang}: {video_path}")
        else:
            logger.error(f"  ❌ Failed to create reel for {lang}")

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 Generation Summary")
    logger.info("=" * 60)
    logger.info(f"Audio files generated: {len(audio_files)}")
    logger.info(f"Video reels created: {len(video_files)}")
    logger.info(f"Languages: {', '.join(video_files.keys())}")
    logger.info("\n✨ All reels generated successfully!")
    logger.info("=" * 60)


def print_usage():
    """Print usage instructions."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         Multilingual Reel Generation System                  ║
╚══════════════════════════════════════════════════════════════╝

📋 Prerequisites:
   1. Record a reference voice sample (10-30 seconds of your voice)
   2. Save it as a WAV file
   3. Update REFERENCE_AUDIO path in this script

🎯 What this does:
   1. Takes your voice sample
   2. Translates your script to multiple languages
   3. Generates speech in each language using YOUR voice
   4. Creates 20-second video reels for each language

🚀 Usage:
   python scripts/demo_multilingual.py

📦 Required packages:
   - TTS (Coqui TTS)
   - transformers (for translation)
   - torch
   - moviepy
   - All other dependencies in requirements.txt

💡 Tip:
   For best results, record your reference voice in a quiet
   environment, speaking clearly and naturally.

═══════════════════════════════════════════════════════════════
    """)


if __name__ == "__main__":
    print_usage()

    # Check if reference audio exists
    reference_path = Path("path/to/your/reference_voice.wav")

    if not reference_path.exists():
        logger.warning("\n⚠️  Reference audio not found!")
        logger.info("Please record your voice and update the REFERENCE_AUDIO path")
        logger.info("in this script before running.")
        sys.exit(1)

    # Run demo
    asyncio.run(demo_multilingual_generation())
