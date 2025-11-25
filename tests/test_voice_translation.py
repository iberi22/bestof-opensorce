"""
Tests for the VoiceTranslationPipeline.

Note: These tests are designed to be lightweight and focus on the pipeline's
structure and orchestration. They mock the heavy AI models to avoid
requiring a GPU or long run times in a CI environment.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_generator.voice_translation import VoiceTranslationPipeline

@pytest.fixture
def mock_audio_file(tmp_path):
    """Create a dummy audio file for testing."""
    audio_path = tmp_path / "test.wav"
    audio_path.touch()
    return str(audio_path)

@patch('video_generator.voice_translation.WHISPER_AVAILABLE', True)
@patch('video_generator.voice_translation.TTS_AVAILABLE', True)
@patch('transformers.MarianMTModel.from_pretrained')
@patch('transformers.MarianTokenizer.from_pretrained')
def test_pipeline_initialization(mock_tokenizer, mock_marian):
    """Test that the VoiceTranslationPipeline can be initialized."""
    with patch('whisper.load_model') as mock_whisper, \
         patch('TTS.api.TTS') as mock_tts:
        mock_tts_instance = Mock()
        mock_tts.return_value.to.return_value = mock_tts_instance
        
        pipeline = VoiceTranslationPipeline()
        assert pipeline is not None
        mock_whisper.assert_called_once()
        # TTS is called through sys.modules mock, so just verify pipeline has tts attribute
        assert hasattr(pipeline, 'tts')

@patch('video_generator.voice_translation.WHISPER_AVAILABLE', True)
@patch('video_generator.voice_translation.TTS_AVAILABLE', True)
def test_transcribe_audio(mock_audio_file):
    """Test the transcription step, mocking the model."""
    with patch('whisper.load_model') as mock_whisper, \
         patch('TTS.api.TTS') as mock_tts:
        mock_tts_instance = Mock()
        mock_tts.return_value.to.return_value = mock_tts_instance
        
        # Arrange
        pipeline = VoiceTranslationPipeline()
        mock_transcribe_result = {'text': 'This is a test.', 'language': 'en'}
        pipeline.whisper_model.transcribe = MagicMock(return_value=mock_transcribe_result)

    # Act
    text, lang = pipeline.transcribe_audio(mock_audio_file)

    # Assert
    assert text == 'This is a test.'
    assert lang == 'en'
    pipeline.whisper_model.transcribe.assert_called_once_with(mock_audio_file, fp16=False)


@patch('video_generator.voice_translation.WHISPER_AVAILABLE', True)
@patch('video_generator.voice_translation.TTS_AVAILABLE', True)
@patch('transformers.MarianMTModel.from_pretrained')
@patch('transformers.MarianTokenizer.from_pretrained')
def test_translate_text(mock_tokenizer, mock_marian):
    """Test the text translation step, mocking the models."""
    with patch('whisper.load_model'), \
         patch('TTS.api.TTS') as mock_tts_class:
        # Setup TTS mock
        mock_tts_instance = Mock()
        mock_tts_class.return_value.to.return_value = mock_tts_instance
        
        # Arrange
        pipeline = VoiceTranslationPipeline()

    # Create proper tensor mocks for tokenizer
    mock_tensor = Mock()
    mock_tensor.to.return_value = mock_tensor
    
    mock_tokenizer_instance = mock_tokenizer.return_value
    mock_model_instance = mock_marian.return_value

    # Mock tokenizer to return tensor-like objects
    mock_tokenizer_instance.return_value = {
        "input_ids": mock_tensor, 
        "attention_mask": mock_tensor
    }
    mock_model_instance.generate.return_value = ["mock_translation_ids"]
    mock_tokenizer_instance.decode.return_value = "Ceci est un test."

    # Act
    translated_text = pipeline.translate_text("This is a test.", source_lang="en", target_lang="fr")

    # Assert
    assert translated_text == "Ceci est un test."
    mock_marian.assert_called_with("Helsinki-NLP/opus-mt-en-fr")
    mock_tokenizer.assert_called_with("Helsinki-NLP/opus-mt-en-fr")


@patch('video_generator.voice_translation.WHISPER_AVAILABLE', True)
@patch('video_generator.voice_translation.TTS_AVAILABLE', True)
def test_synthesize_speech(mock_audio_file, tmp_path):
    """Test the speech synthesis step, mocking the TTS model."""
    with patch('whisper.load_model') as mock_whisper, \
         patch('TTS.api.TTS') as mock_tts:
        mock_tts_instance = Mock()
        mock_tts.return_value.to.return_value = mock_tts_instance
        
        # Arrange
        pipeline = VoiceTranslationPipeline()
        mock_tts_instance = pipeline.tts
        output_path = tmp_path / "output.wav"

    # Act
    result_path = pipeline.synthesize_speech("Ceci est un test.", mock_audio_file, str(output_path), language="fr")

    # Assert
    assert result_path == str(output_path)
    mock_tts_instance.tts_to_file.assert_called_once_with(
        text="Ceci est un test.",
        file_path=str(output_path),
        speaker_wav=mock_audio_file,
        language="fr"
    )

@patch('video_generator.voice_translation.WHISPER_AVAILABLE', True)
@patch('video_generator.voice_translation.TTS_AVAILABLE', True)
@patch('video_generator.voice_translation.VoiceTranslationPipeline.transcribe_audio')
@patch('video_generator.voice_translation.VoiceTranslationPipeline.translate_text')
@patch('video_generator.voice_translation.VoiceTranslationPipeline.synthesize_speech')
def test_full_voice_translation_pipeline(mock_synthesize, mock_translate, mock_transcribe):
    """Test the end-to-end voice translation pipeline by mocking each step."""
    with patch('whisper.load_model'), \
         patch('TTS.api.TTS') as mock_tts:
        mock_tts_instance = Mock()
        mock_tts.return_value.to.return_value = mock_tts_instance
        
        # Arrange
        pipeline = VoiceTranslationPipeline()

    mock_audio = "/path/to/audio.wav"
    output_path = "/path/to/output.wav"

    mock_transcribe.return_value = ("This is a test", "en")
    mock_translate.return_value = "Ceci est un test"
    mock_synthesize.return_value = output_path

    # Act
    result = pipeline.translate_voice(mock_audio, "fr", output_path)

    # Assert
    mock_transcribe.assert_called_once_with(mock_audio)
    mock_translate.assert_called_once_with("This is a test", "en", "fr")
    mock_synthesize.assert_called_once_with("Ceci est un test", mock_audio, output_path, "fr")

    assert result is not None
    assert result["original_text"] == "This is a test"
    assert result["translated_text"] == "Ceci est un test"
    assert result["audio_path"] == output_path

