"""
Image Generator using Foundry Local with Nano Banana 2.

This module generates explanatory images for repositories to help visualize:
- Architecture diagrams
- Problem-solution flows
- Key concepts and features
"""

import logging
import os
from typing import Optional, Dict, Any, List
from pathlib import Path
import base64
from io import BytesIO


class ImageGenerator:
    """
    Generates explanatory images using Foundry Local with Nano Banana 2 model.

    Nano Banana 2 is a lightweight image generation model that runs locally,
    perfect for creating diagrams and conceptual illustrations.
    """

    def __init__(self, model_name: str = "nano-banana-2", output_dir: str = "output/images"):
        """
        Initialize Image Generator.

        Args:
            model_name: Foundry model alias for image generation.
            output_dir: Directory to save generated images.
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Foundry Local for image generation
        try:
            from foundry_local import FoundryLocalManager
            self.manager = FoundryLocalManager(self.model_name)
            self.logger.info(f"Initialized Foundry Local with model: {self.model_name}")
        except ImportError:
            self.logger.error("foundry-local-sdk is required for image generation")
            raise ImportError("Install foundry-local-sdk: pip install foundry-local-sdk")
        except Exception as e:
            self.logger.error(f"Failed to initialize Foundry Local: {e}")
            raise

    def generate_architecture_diagram(
        self,
        repo_data: Dict[str, Any],
        script_data: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Generate an architecture diagram for the repository.

        Args:
            repo_data: Repository metadata from GitHub.
            script_data: Optional script data with analysis.

        Returns:
            Path to generated image file, or None if generation failed.
        """
        repo_name = repo_data.get("name", "unknown")
        description = repo_data.get("description", "")

        # Build prompt for architecture diagram
        prompt = self._build_architecture_prompt(repo_name, description, script_data)

        return self._generate_image(
            prompt=prompt,
            filename=f"{repo_name}_architecture.png"
        )

    def generate_problem_solution_flow(
        self,
        repo_data: Dict[str, Any],
        script_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate a problem-solution flow diagram.

        Args:
            repo_data: Repository metadata.
            script_data: Script data containing hook and solution.

        Returns:
            Path to generated image file, or None if generation failed.
        """
        repo_name = repo_data.get("name", "unknown")
        hook = script_data.get("hook", "")
        solution = script_data.get("solution", "")

        prompt = f"""
        Create a clean, modern problem-solution flow diagram:

        Problem: {hook}
        Solution: {solution}

        Style: Minimalist, professional, with clear arrows showing the transformation.
        Use a color scheme: Problem (red/orange tones) → Solution (green/blue tones).
        Include icons or simple illustrations.
        """

        return self._generate_image(
            prompt=prompt,
            filename=f"{repo_name}_flow.png"
        )

    def generate_feature_showcase(
        self,
        repo_data: Dict[str, Any],
        features: List[str]
    ) -> Optional[str]:
        """
        Generate a visual showcase of key features.

        Args:
            repo_data: Repository metadata.
            features: List of key features to visualize.

        Returns:
            Path to generated image file, or None if generation failed.
        """
        repo_name = repo_data.get("name", "unknown")
        features_text = "\n".join([f"- {f}" for f in features[:5]])  # Limit to 5

        prompt = f"""
        Create a modern feature showcase infographic for: {repo_name}

        Features:
        {features_text}

        Style: Clean, modern UI design with icons for each feature.
        Layout: Grid or card-based layout.
        Color scheme: Professional tech colors (blues, purples, gradients).
        """

        return self._generate_image(
            prompt=prompt,
            filename=f"{repo_name}_features.png"
        )

    def _build_architecture_prompt(
        self,
        repo_name: str,
        description: str,
        script_data: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build a detailed prompt for architecture diagram generation.

        Args:
            repo_name: Repository name.
            description: Repository description.
            script_data: Optional script analysis data.

        Returns:
            Formatted prompt string.
        """
        base_prompt = f"""
        Create a clean, professional architecture diagram for: {repo_name}

        Description: {description}
        """

        if script_data:
            solution = script_data.get("solution", "")
            base_prompt += f"\n\nHow it works: {solution}"

        base_prompt += """

        Style: Modern tech diagram with:
        - Clear component boxes
        - Labeled arrows showing data flow
        - Color-coded sections (frontend, backend, database, etc.)
        - Minimalist, professional aesthetic
        - Tech stack icons if applicable
        """

        return base_prompt

    def _generate_image(self, prompt: str, filename: str) -> Optional[str]:
        """
        Generate image using Foundry Local.

        Args:
            prompt: Text prompt for image generation.
            filename: Output filename.

        Returns:
            Path to saved image file, or None if failed.
        """
        try:
            self.logger.info(f"Generating image: {filename}")

            # Get model info and endpoint
            model_info = self.manager.get_model_info(self.model_name)

            # Note: Nano Banana 2 integration depends on Foundry Local's API
            # This is a placeholder implementation - adjust based on actual API

            # For now, we'll use OpenAI-compatible endpoint if available
            try:
                import openai
                from PIL import Image
                import requests

                client = openai.OpenAI(
                    base_url=self.manager.endpoint,
                    api_key=self.manager.api_key
                )

                # Generate image (API may vary)
                response = client.images.generate(
                    model=model_info.id,
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )

                # Download and save image
                image_url = response.data[0].url
                image_data = requests.get(image_url).content

                output_path = self.output_dir / filename
                with open(output_path, 'wb') as f:
                    f.write(image_data)

                self.logger.info(f"Image saved to: {output_path}")
                return str(output_path)

            except Exception as e:
                self.logger.warning(f"OpenAI-style API failed: {e}")
                self.logger.info("Falling back to placeholder generation")
                return self._generate_placeholder(filename, prompt)

        except Exception as e:
            self.logger.error(f"Failed to generate image: {e}")
            return None

    def _generate_placeholder(self, filename: str, prompt: str) -> str:
        """
        Generate a placeholder image when actual generation fails.

        This creates a simple text-based placeholder for development/testing.

        Args:
            filename: Output filename.
            prompt: Original prompt (for reference).

        Returns:
            Path to placeholder image.
        """
        try:
            from PIL import Image, ImageDraw, ImageFont

            # Create a simple placeholder
            img = Image.new('RGB', (1024, 1024), color=(45, 55, 72))
            draw = ImageDraw.Draw(img)

            # Add text
            text = f"Placeholder\n{filename}\n\n(Nano Banana 2 integration pending)"

            # Use default font
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            # Center text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((1024 - text_width) // 2, (1024 - text_height) // 2)

            draw.text(position, text, fill=(255, 255, 255), font=font)

            output_path = self.output_dir / filename
            img.save(output_path)

            self.logger.info(f"Placeholder image saved to: {output_path}")
            return str(output_path)

        except Exception as e:
            self.logger.error(f"Failed to create placeholder: {e}")
            return None
