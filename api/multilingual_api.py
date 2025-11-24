"""
Flask API for multilingual reel generation.

Endpoints:
- POST /api/generate-multilingual-reels - Generate reels in multiple languages
- GET /api/languages - Get supported languages
- GET /api/status/<job_id> - Check generation status
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
import os
import sys
from pathlib import Path
import json
from werkzeug.utils import secure_filename

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_generator.voice_cloning import VoiceCloner, TextTranslator, MultilingualReelGenerator
from video_generator.reel_creator import ReelCreator

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('blog/assets/videos')
AUDIO_FOLDER = Path('blog/assets/audio/multilingual')

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages."""
    try:
        voice_cloner = VoiceCloner()
        languages = voice_cloner.get_supported_languages()

        # Language metadata
        language_info = {
            "en": {"name": "English", "flag": "🇺🇸"},
            "es": {"name": "Español", "flag": "🇪🇸"},
            "fr": {"name": "Français", "flag": "🇫🇷"},
            "de": {"name": "Deutsch", "flag": "🇩🇪"},
            "it": {"name": "Italiano", "flag": "🇮🇹"},
            "pt": {"name": "Português", "flag": "🇵🇹"},
            "ru": {"name": "Русский", "flag": "🇷🇺"},
            "zh-cn": {"name": "中文", "flag": "🇨🇳"},
            "ja": {"name": "日本語", "flag": "🇯🇵"},
            "ar": {"name": "العربية", "flag": "🇸🇦"},
        }

        result = []
        for lang in languages:
            if lang in language_info:
                result.append({
                    "code": lang,
                    **language_info[lang]
                })

        return jsonify({"languages": result})

    except Exception as e:
        logger.error(f"Error getting languages: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate-multilingual-reels', methods=['POST'])
def generate_multilingual_reels():
    """
    Generate video reels in multiple languages.

    Expected form data:
    - audio: Audio file (reference voice)
    - script: Text script (English)
    - languages: JSON array of target language codes
    - repo_name: (optional) Repository name
    """
    try:
        # Validate request
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        if 'script' not in request.form:
            return jsonify({"error": "No script provided"}), 400

        audio_file = request.files['audio']
        script = request.form['script']
        languages_json = request.form.get('languages', '["en"]')
        repo_name = request.form.get('repo_name', 'demo-project')

        # Parse languages
        try:
            target_languages = json.loads(languages_json)
        except:
            target_languages = ["en"]

        # Validate audio file
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400

        if not allowed_file(audio_file.filename):
            return jsonify({"error": "Invalid audio file format"}), 400

        # Save reference audio
        filename = secure_filename(audio_file.filename)
        reference_audio_path = UPLOAD_FOLDER / f"reference_{filename}"
        audio_file.save(str(reference_audio_path))

        logger.info(f"Generating reels for {len(target_languages)} languages")
        logger.info(f"Script: {script[:100]}...")

        # Generate multilingual audio
        generator = MultilingualReelGenerator(
            reference_audio=str(reference_audio_path),
            output_dir=str(AUDIO_FOLDER)
        )

        audio_results = generator.generate_multilingual_audio(
            script=script,
            repo_name=repo_name,
            target_languages=target_languages
        )

        if not audio_results:
            return jsonify({"error": "Failed to generate audio"}), 500

        # Generate video reels for each language
        video_results = {}
        reel_creator = ReelCreator(output_dir=str(OUTPUT_FOLDER))

        # Placeholder images (in real scenario, these would come from the blog post)
        placeholder_images = {
            'architecture': 'blog/assets/images/placeholder/architecture.png',
            'flow': 'blog/assets/images/placeholder/flow.png',
            'screenshot': 'blog/assets/images/placeholder/screenshot.png'
        }

        script_data = {
            'hook': script[:100],
            'solution': script,
            'verdict': 'Check it out!'
        }

        for lang, audio_path in audio_results.items():
            try:
                video_path = reel_creator.create_reel(
                    repo_name=f"{repo_name}-{lang}",
                    script_data=script_data,
                    images=placeholder_images,
                    audio_path=audio_path
                )

                if video_path:
                    video_results[lang] = video_path
                    logger.info(f"✅ Video created for {lang}: {video_path}")

            except Exception as e:
                logger.error(f"Failed to create video for {lang}: {e}")

        # Cleanup reference audio
        try:
            reference_audio_path.unlink()
        except:
            pass

        return jsonify({
            "success": True,
            "message": f"Generated {len(video_results)} reels",
            "audio_files": audio_results,
            "video_files": video_results,
            "languages": list(video_results.keys())
        })

    except Exception as e:
        logger.error(f"Error generating reels: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/api/download/<lang>/<filename>', methods=['GET'])
def download_file(lang, filename):
    """Download generated video file."""
    try:
        file_path = OUTPUT_FOLDER / filename

        if not file_path.exists():
            return jsonify({"error": "File not found"}), 404

        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "multilingual-reel-api"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
