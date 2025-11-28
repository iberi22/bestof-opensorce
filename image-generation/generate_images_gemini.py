import os
import sys
import time
import google.generativeai as genai
from pathlib import Path
import re

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logging.error("GOOGLE_API_KEY not found in environment variables")
        return None

    genai.configure(api_key=api_key)
    return True

def generate_image_gemini(prompt, output_path):
    """Generates an image using Google Gemini (Imagen 3)."""
    try:
        # Check for available models that support image generation
        # Note: The specific model name for Imagen 3 via API might vary (e.g., 'models/imagen-3.0-generate-001')
        # We will try a few known ones or default to the latest.

        model_name = 'models/imagen-3.0-generate-001'

        # Fallback logic could be added here if listing models was possible and reliable

        logging.info(f"🎨 Generating image with prompt: {prompt[:80]}...")

        # The python SDK for Imagen is slightly different than text generation.
        # As of late 2024/2025, it might be genai.ImageGenerationModel

        try:
            image_model = genai.ImageGenerationModel(model_name)
            response = image_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="block_only_high",
                person_generation="allow_adult"
            )

            if response.images:
                image = response.images[0]
                image.save(output_path)
                logging.info(f"✅ Image saved to: {output_path}")
                return True
            else:
                logging.error("❌ No images returned in response")
                return False

        except AttributeError:
            # Fallback for older SDK versions or different API structure
            # Some versions use genai.generate_content with specific tools
            logging.warning("⚠️ ImageGenerationModel not found, trying legacy/alternative method...")
            return False

    except Exception as e:
        logging.error(f"❌ Error generating image with Gemini: {e}")
        return False

def extract_frontmatter(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    return {
        'frontmatter': parts[1],
        'content': parts[2],
        'file': md_file
    }

def parse_metadata(frontmatter):
    lines = frontmatter.strip().split('\n')
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"\'')
    return data

def create_prompt(title, repo, language, description):
    return (
        f"Professional 3D infographic for '{title}', {description}. "
        f"Visualizing real-world application and solution architecture. "
        f"High-end digital art, isometric view, sleek modern design, "
        f"vibrant colors, professional lighting, sharp focus, 16:9 aspect ratio, "
        f"no text, clean composition, tech blog header style."
    )

def process_blog_posts():
    if not setup_gemini():
        return

    blog_dir = Path("website/src/content/blog")

    for md_file in blog_dir.rglob("index.md"):
        # Check if header.png exists
        image_path = md_file.parent / "header.png"
        if image_path.exists():
            continue

        logging.info(f"📝 Processing missing image for: {md_file.parent.name}")

        data = extract_frontmatter(md_file)
        if not data:
            continue

        meta = parse_metadata(data['frontmatter'])
        title = meta.get('title', '')
        repo = meta.get('repo', '')
        language = meta.get('language', '')
        description = meta.get('description', '')

        if not title:
            continue

        prompt = create_prompt(title, repo, language, description)

        if generate_image_gemini(prompt, image_path):
            # Wait to avoid rate limits
            time.sleep(10)
        else:
            logging.error(f"Failed to generate image for {title}")

if __name__ == "__main__":
    process_blog_posts()
