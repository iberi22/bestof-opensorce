"""
Unit tests for Image Generator module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.image_gen.image_generator import ImageGenerator


@pytest.fixture
def mock_foundry():
    """Mock Foundry Local Manager."""
    with patch.dict('sys.modules', {'foundry_local': MagicMock()}):
        with patch('src.image_gen.image_generator.FoundryLocalManager') as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.endpoint = "http://localhost:8000"
            mock_manager.api_key = "test-key"

            mock_model_info = MagicMock()
            mock_model_info.id = "nano-banana-2"
            mock_manager.get_model_info.return_value = mock_model_info

            mock_manager_class.return_value = mock_manager

            yield mock_manager


@pytest.fixture
def image_generator(mock_foundry, tmp_path):
    """Create ImageGenerator instance with mocked Foundry."""
    generator = ImageGenerator(
        model_name="nano-banana-2",
        output_dir=str(tmp_path / "images")
    )
    return generator


class TestImageGenerator:
    """Test suite for ImageGenerator class."""

    def test_initialization(self, tmp_path):
        """Test ImageGenerator initialization."""
        with patch('src.image_gen.image_generator.FoundryLocalManager'):
            generator = ImageGenerator(output_dir=str(tmp_path / "images"))

            assert generator.model_name == "nano-banana-2"
            assert generator.output_dir.exists()

    def test_initialization_creates_output_dir(self, tmp_path):
        """Test that initialization creates output directory."""
        output_dir = tmp_path / "test_images"

        with patch('src.image_gen.image_generator.FoundryLocalManager'):
            generator = ImageGenerator(output_dir=str(output_dir))

            assert output_dir.exists()

    def test_initialization_without_foundry_sdk(self, tmp_path):
        """Test initialization fails without foundry-local-sdk."""
        with patch('src.image_gen.image_generator.FoundryLocalManager', side_effect=ImportError):
            with pytest.raises(ImportError, match="foundry-local-sdk"):
                ImageGenerator(output_dir=str(tmp_path))

    def test_generate_architecture_diagram(self, image_generator, mock_foundry):
        """Test architecture diagram generation."""
        repo_data = {
            "name": "test-repo",
            "description": "A test repository"
        }

        with patch.object(image_generator, '_generate_image', return_value="/path/to/image.png") as mock_gen:
            result = image_generator.generate_architecture_diagram(repo_data)

            assert result == "/path/to/image.png"
            mock_gen.assert_called_once()

            # Verify prompt contains repo info
            call_args = mock_gen.call_args
            assert "test-repo" in call_args[1]['prompt']
            assert "A test repository" in call_args[1]['prompt']

    def test_generate_problem_solution_flow(self, image_generator):
        """Test problem-solution flow diagram generation."""
        repo_data = {"name": "test-repo"}
        script_data = {
            "hook": "Developers struggle with deployment",
            "solution": "Automated CI/CD pipeline"
        }

        with patch.object(image_generator, '_generate_image', return_value="/path/to/flow.png") as mock_gen:
            result = image_generator.generate_problem_solution_flow(repo_data, script_data)

            assert result == "/path/to/flow.png"

    def test_build_architecture_prompt_basic(self, image_generator):
        """Test architecture prompt building without script data."""
        prompt = image_generator._build_architecture_prompt(
            "test-repo",
            "A test repository",
            None
        )

        assert "test-repo" in prompt
        assert "A test repository" in prompt
        assert "architecture diagram" in prompt.lower()
