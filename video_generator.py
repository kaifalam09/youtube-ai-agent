"""
Generates a short vertical video from a text script:
  1. Converts script to speech (gTTS)
  2. Renders text captions over a simple animated background
  3. Hard-caps the final video at config.MAX_VIDEO_SECONDS
"""
import os
import time
import textwrap
from gtts import gTTS
from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    TextClip,
)
import config


def _make_audio(script: str) -> str:
    audio_path = os.path.join(config.OUTPUT_DIR, f"narration_{int(time.time())}.mp3")
    tts = gTTS(text=script, lang="en")
    tts.save(audio_path)
    return audio_path


def _wrap_caption(text: str, width: int = 28) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def generate_video(script: str, filename: str = None) -> str:
    """
    Build a vertical video with narration + captions.
    Returns the path to the final .mp4 file.
    Duration is hard-capped at config.MAX_VIDEO_SECONDS regardless of
    how long the narration audio turns out to be.
    """
    audio_path = _make_audio(script)
    audio_clip = AudioFileClip(audio_path)

    duration = min(audio_clip.duration, config.MAX_VIDEO_SECONDS)
    audio_clip = audio_clip.subclip(0, duration)

    background = ColorClip(
        size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
        color=(20, 20, 30),
        duration=duration,
    )

    caption = _wrap_caption(script)
    text_clip = (
        TextClip(
            caption,
            fontsize=64,
            color="white",
            size=(config.VIDEO_WIDTH - 120, None),
            method="caption",
            align="center",
        )
        .set_position("center")
        .set_duration(duration)
    )

    final = CompositeVideoClip([background, text_clip]).set_audio(audio_clip)

    if not filename:
        filename = f"video_{int(time.time())}.mp4"
    output_path = os.path.join(config.OUTPUT_DIR, filename)

    final.write_videofile(
        output_path,
        fps=config.FPS,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None,
    )

    # cleanup intermediate audio
    audio_clip.close()
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return output_path
