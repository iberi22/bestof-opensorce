"""
Reel Creator module.

Generates 20-second vertical videos (9:16) for social media reels.
"""

import logging
import os
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple
from moviepy import (
    VideoFileClip, ImageClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip, AudioFileClip
)
from moviepy.video.fx import Resize, Crop

class ReelCreator:
    """
    Creates 20-second video reels from blog post content.
    """

    def __init__(self, output_dir: str = "blog/assets/videos"):
        """
        Initialize ReelCreator.

        Args:
            output_dir: Directory to save generated videos.
        """
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Video settings (Vertical 9:16)
        self.width = 1080
        self.height = 1920
        self.fps = 30
        self.duration = 20

        # Colors
        self.bg_color = (31, 41, 55) # Dark gray/blue
        self.text_color = 'white'
        self.accent_color = '#2563eb' # Blue

    def create_reel(
        self,
        repo_name: str,
        script_data: Dict[str, Any],
        images: Dict[str, str],
        audio_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a 20-second reel.

        Timeline:
        00-03s: Intro (Title + Logo)
        03-08s: Problem (Flow Diagram)
        08-13s: Solution (Screenshot)
        13-17s: Architecture (Diagram)
        17-20s: Outro (CTA)
        """
        self.logger.info(f"Creating reel for {repo_name}...")

        try:
            clips = []

            # 1. Intro (0-3s)
            intro_clip = self._create_intro(repo_name, duration=3)
            clips.append(intro_clip)

            # 2. Problem (3-8s)
            problem_img = images.get('flow')
            problem_text = script_data.get('hook', 'Problem Analysis')
            problem_clip = self._create_section(
                "The Problem",
                problem_text,
                problem_img,
                duration=5
            )
            clips.append(problem_clip)

            # 3. Solution (8-13s)
            solution_img = images.get('screenshot')
            solution_text = script_data.get('solution', 'The Solution')
            solution_clip = self._create_section(
                "The Solution",
                solution_text,
                solution_img,
                duration=5
            )
            clips.append(solution_clip)

            # 4. Architecture (13-17s)
            arch_img = images.get('architecture')
            arch_text = "How it Works"
            arch_clip = self._create_section(
                "Architecture",
                arch_text,
                arch_img,
                duration=4
            )
            clips.append(arch_clip)

            # 5. Outro (17-20s)
            outro_clip = self._create_outro(duration=3)
            clips.append(outro_clip)

            # Concatenate
            final_video = concatenate_videoclips(clips, method="compose")

            # Add Audio if provided
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                # Loop or cut audio to fit video
                if audio.duration < self.duration:
                    # If audio is shorter, we might need to loop or silence (simple logic for now)
                    pass
                else:
                    audio = audio.subclip(0, self.duration)
                final_video = final_video.set_audio(audio)

            # Write file
            output_filename = f"{repo_name.lower().replace(' ', '-')}-reel.mp4"
            output_path = self.output_dir / output_filename

            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                logger=None # Reduce noise
            )

            self.logger.info(f"Reel created successfully: {output_path}")
            return str(output_path)

        except Exception as e:
            self.logger.error(f"Failed to create reel: {e}", exc_info=True)
            return None

    def _create_intro(self, title: str, duration: int) -> CompositeVideoClip:
        """Create intro section."""
        # Background
        bg = ColorClip(size=(self.width, self.height), color=self.bg_color, duration=duration)

        # Title Text
        try:
            txt_clip = TextClip(
                text=title,
                font_size=70,
                color=self.text_color,
                font='Arial-Bold',
                size=(self.width - 100, None),
                method='caption'
            ).with_position('center').with_duration(duration)

            return CompositeVideoClip([bg, txt_clip])
        except Exception as e:
            self.logger.warning(f"TextClip failed: {e}")
            return bg

    def _create_section(
        self,
        header: str,
        body: str,
        image_path: Optional[str],
        duration: int
    ) -> CompositeVideoClip:
        """Create a content section with image and text overlay."""

        # Background
        bg = ColorClip(size=(self.width, self.height), color=self.bg_color, duration=duration)
        layers = [bg]

        # Image
        if image_path and os.path.exists(image_path):
            img_clip = ImageClip(image_path).with_duration(duration)

            # Resize to fit width, maintain aspect ratio
            # MoviePy v2 uses with_effects for resizing
            img_clip = img_clip.with_effects([Resize(width=self.width)])

            # Center vertically
            img_clip = img_clip.with_position('center')
            layers.append(img_clip)

        # Header Text (Top)
        try:
            header_clip = TextClip(
                text=header,
                font_size=60,
                color=self.accent_color,
                font='Arial-Bold',
                bg_color='rgba(0,0,0,0.5)',
                size=(self.width, None),
                method='caption'
            ).with_position(('center', 100)).with_duration(duration)
            layers.append(header_clip)

            # Body Text (Bottom Overlay)
            if len(body) > 100:
                body = body[:97] + "..."

            body_clip = TextClip(
                text=body,
                font_size=40,
                color=self.text_color,
                font='Arial',
                bg_color='rgba(0,0,0,0.7)',
                size=(self.width - 100, None),
                method='caption'
            ).with_position(('center', self.height - 300)).with_duration(duration)
            layers.append(body_clip)

        except Exception:
            pass

        return CompositeVideoClip(layers)

    def _create_outro(self, duration: int) -> CompositeVideoClip:
        """Create outro section."""
        bg = ColorClip(size=(self.width, self.height), color=self.bg_color, duration=duration)

        try:
            txt_clip = TextClip(
                text="Link in Bio\nCheck the Blog!",
                font_size=80,
                color=self.text_color,
                font='Arial-Bold',
                size=(self.width - 100, None),
                method='caption'
            ).with_position('center').with_duration(duration)

            return CompositeVideoClip([bg, txt_clip])
        except Exception:
            return bg
