import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip
import os

class ContentRenderer:
    def __init__(self):
        pass

    async def generate_audio(self, text, output_file="output/narration.mp3", voice="en-US-ChristopherNeural"):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return output_file

    def compose_video(self, video_path, audio_path, output_path):
        try:
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)

            # Adjust video duration to match audio
            # If video is shorter than audio, we might need to loop or slow down.
            # For now, let's just loop the video if it's too short, or cut audio if too long (not ideal).
            # Better strategy: Loop the video content or freeze the last frame.

            if video_clip.duration < audio_clip.duration:
                # Loop video to match audio
                video_clip = video_clip.loop(duration=audio_clip.duration)
            else:
                # Cut video to match audio
                video_clip = video_clip.subclip(0, audio_clip.duration)

            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            video_clip.close()
            audio_clip.close()
            return True
        except Exception as e:
            print(f"Error composing video: {e}")
            return False
