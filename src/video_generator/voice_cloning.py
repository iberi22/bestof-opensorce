"""
Voice Cloning and Multi-language Translation System.

Uses local models for voice cloning and translation:
- Coqui TTS (XTTS-v2) for voice cloning
- Whisper for transcription
- MarianMT for translation
"""

import logging
import torch
from pathlib import Path
from typing import Optional, List, Dict
import numpy as np

# Check if TTS is available
try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logging.warning("Coqui TTS not available. Install with: pip install TTS")

# Check if transformers is available for translation
try:
    from transformers import MarianMTModel, MarianTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers not available. Install with: pip install transformers")


class VoiceCloner:
    """
    Voice cloning system using Coqui TTS XTTS-v2.
    Supports voice cloning and multi-language synthesis.
    """

    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        """
        Initialize Voice Cloner.

        Args:
            model_name: TTS model to use (default: XTTS-v2 for multilingual support).
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.tts = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if not TTS_AVAILABLE:
            raise ImportError("Coqui TTS is required. Install with: pip install TTS")

        self.logger.info(f"Initializing TTS model: {model_name} on {self.device}")
        self.tts = TTS(model_name).to(self.device)

        # Supported languages for XTTS-v2
        self.supported_languages = [
            "en", "es", "fr", "de", "it", "pt", "pl", "tr",
            "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"
        ]

    def clone_voice(
        self,
        text: str,
        reference_audio: str,
        output_path: str,
        language: str = "en"
    ) -> Optional[str]:
        """
        Clone voice and generate speech in specified language.

        Args:
            text: Text to synthesize.
            reference_audio: Path to reference audio file (your voice sample).
            output_path: Path to save generated audio.
            language: Target language code (e.g., 'en', 'es', 'fr').

        Returns:
            Path to generated audio file, or None if failed.
        """
        try:
            if language not in self.supported_languages:
                self.logger.warning(f"Language {language} not supported. Using 'en'.")
                language = "en"

            self.logger.info(f"Generating speech in {language} with voice cloning...")

            # Generate speech with voice cloning
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=reference_audio,
                language=language
            )

            self.logger.info(f"Voice cloned audio saved to {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Failed to clone voice: {e}", exc_info=True)
            return None

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return self.supported_languages


class TextTranslator:
    """
    Text translation system using MarianMT models.
    Supports multiple language pairs.
    """

    def __init__(self):
        """Initialize Text Translator."""
        self.logger = logging.getLogger(__name__)
        self.models = {}
        self.tokenizers = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("Transformers is required. Install with: pip install transformers")

        # Common translation pairs
        self.language_pairs = {
            "en-es": "Helsinki-NLP/opus-mt-en-es",
            "en-fr": "Helsinki-NLP/opus-mt-en-fr",
            "en-de": "Helsinki-NLP/opus-mt-en-de",
            "en-it": "Helsinki-NLP/opus-mt-en-it",
            "en-pt": "Helsinki-NLP/opus-mt-en-pt",
            "en-ru": "Helsinki-NLP/opus-mt-en-ru",
            "en-zh": "Helsinki-NLP/opus-mt-en-zh",
            "en-ja": "Helsinki-NLP/opus-mt-en-jap",
            "en-ar": "Helsinki-NLP/opus-mt-en-ar",
        }

    def _load_model(self, source_lang: str, target_lang: str) -> bool:
        """
        Load translation model for language pair.

        Args:
            source_lang: Source language code.
            target_lang: Target language code.

        Returns:
            True if model loaded successfully.
        """
        pair_key = f"{source_lang}-{target_lang}"

        if pair_key in self.models:
            return True

        if pair_key not in self.language_pairs:
            self.logger.error(f"Translation pair {pair_key} not supported")
            return False

        try:
            model_name = self.language_pairs[pair_key]
            self.logger.info(f"Loading translation model: {model_name}")

            self.tokenizers[pair_key] = MarianTokenizer.from_pretrained(model_name)
            self.models[pair_key] = MarianMTModel.from_pretrained(model_name).to(self.device)

            return True

        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False

    def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "es"
    ) -> Optional[str]:
        """
        Translate text from source to target language.

        Args:
            text: Text to translate.
            source_lang: Source language code.
            target_lang: Target language code.

        Returns:
            Translated text, or None if failed.
        """
        try:
            pair_key = f"{source_lang}-{target_lang}"

            # Load model if not already loaded
            if not self._load_model(source_lang, target_lang):
                return None

            # Tokenize
            inputs = self.tokenizers[pair_key](text, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Translate
            translated = self.models[pair_key].generate(**inputs)
            translated_text = self.tokenizers[pair_key].decode(translated[0], skip_special_tokens=True)

            self.logger.info(f"Translated ({source_lang} -> {target_lang}): {text[:50]}... -> {translated_text[:50]}...")
            return translated_text

        except Exception as e:
            self.logger.error(f"Translation failed: {e}", exc_info=True)
            return None

    def get_supported_pairs(self) -> List[str]:
        """Get list of supported translation pairs."""
        return list(self.language_pairs.keys())


class MultilingualReelGenerator:
    """
    Generates reels in multiple languages using voice cloning.
    """

    def __init__(self, reference_audio: str, output_dir: str = "blog/assets/audio/multilingual"):
        """
        Initialize Multilingual Reel Generator.

        Args:
            reference_audio: Path to reference audio (your voice sample).
            output_dir: Directory to save generated audio files.
        """
        self.logger = logging.getLogger(__name__)
        self.reference_audio = reference_audio
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.voice_cloner = VoiceCloner()
        self.translator = TextTranslator()

    def generate_multilingual_audio(
        self,
        script: str,
        repo_name: str,
        target_languages: List[str] = ["en", "es", "fr", "de"]
    ) -> Dict[str, str]:
        """
        Generate audio in multiple languages.

        Args:
            script: Original script text (in English).
            repo_name: Repository name for filename.
            target_languages: List of target language codes.

        Returns:
            Dictionary mapping language code to audio file path.
        """
        results = {}
        safe_name = repo_name.lower().replace(" ", "-").replace("/", "-")

        for lang in target_languages:
            try:
                # Translate if not English
                if lang == "en":
                    text = script
                else:
                    self.logger.info(f"Translating to {lang}...")
                    text = self.translator.translate(script, "en", lang)
                    if not text:
                        self.logger.warning(f"Translation to {lang} failed, skipping")
                        continue

                # Generate audio with voice cloning
                output_filename = f"{safe_name}-{lang}.wav"
                output_path = str(self.output_dir / output_filename)

                audio_path = self.voice_cloner.clone_voice(
                    text=text,
                    reference_audio=self.reference_audio,
                    output_path=output_path,
                    language=lang
                )

                if audio_path:
                    results[lang] = audio_path
                    self.logger.info(f"✅ Generated audio for {lang}: {audio_path}")

            except Exception as e:
                self.logger.error(f"Failed to generate audio for {lang}: {e}")

        return results
