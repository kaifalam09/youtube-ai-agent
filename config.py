"""
Central configuration for the YouTube AI Agent.
"""
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Hard cap on generated video length in seconds.
# This is intentional and should not be removed — long auto-generated
# videos are far more likely to look spammy / violate platform policy.
MAX_VIDEO_SECONDS = 50

# Video output settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # vertical, good for Shorts
FPS = 30

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# YouTube OAuth files
CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
