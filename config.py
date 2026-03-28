"""
config.py — App-wide constants, environment loading, and prompt templates.
All service modules import from here to avoid scattered magic strings.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
load_dotenv(find_dotenv())

HUGGINGFACE_API_TOKEN: str = os.getenv("HUGGINGFACE_API_TOKEN", "")
GROK_API_KEY: str = os.getenv("GROK_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent
TEMP_DIR = ROOT_DIR / "temp"
LOGS_DIR = ROOT_DIR / "logs"
ASSETS_DIR = ROOT_DIR / "img"

# Ensure runtime directories exist
TEMP_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------------
BLIP_MODEL_ID = "Salesforce/blip-image-captioning-base"

# Grok (xAI) — Primary (if available)
GROK_BASE_URL = "https://api.x.ai/v1"
GROK_MODEL = "grok-4"
GROK_TEMPERATURE = 0.9

# Groq — High Speed Alternative
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.8 / 1.0  # Normalized

GROK_MAX_RETRIES = 3
GROQ_MAX_RETRIES = 3

# HuggingFace TTS voices
TTS_VOICES: dict[str, dict[str, str]] = {
    "🎙️ Emma (Female, Neutral)": {
        "url": "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits",
        "description": "Clear, neutral female voice (LJSpeech)",
    },
    "🔊 Ryan (Male, US English)": {
        "url": "https://api-inference.huggingface.co/models/facebook/mms-tts-eng",
        "description": "Warm male US-English voice (MMS-TTS)",
    },
    "🎤 Jenny (Female, Expressive)": {
        "url": "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_tacotron2_raw_phn_tacotron_g2p_en_no_space_train.loss.best",
        "description": "Expressive female, Tacotron2",
    },
    "📢 Alex (Male, UK English)": {
        "url": "https://api-inference.huggingface.co/models/facebook/mms-tts-eng",
        "description": "British-inflected male voice",
    },
}
DEFAULT_VOICE = "🎙️ Emma (Female, Neutral)"

# ---------------------------------------------------------------------------
# Story styles
# ---------------------------------------------------------------------------
STORY_STYLES: dict[str, dict[str, str]] = {
    "🎭 Dramatic": {
        "label": "Dramatic",
        "instruction": (
            "Write in a cinematic, emotionally charged style with vivid imagery "
            "and powerful language."
        ),
    },
    "😂 Funny": {
        "label": "Funny",
        "instruction": (
            "Write in a humorous, lighthearted tone with witty observations, "
            "unexpected twists, and playful language."
        ),
    },
    "😱 Horror": {
        "label": "Horror",
        "instruction": (
            "Write in a suspenseful, dark tone with eerie atmosphere, "
            "building dread and an unsettling twist."
        ),
    },
    "💕 Romantic": {
        "label": "Romantic",
        "instruction": (
            "Write in a warm, tender, and poetic style full of emotion, "
            "connection, and heartfelt moments."
        ),
    },
    "💪 Motivational": {
        "label": "Motivational",
        "instruction": (
            "Write in an uplifting, inspiring tone that empowers the reader, "
            "highlighting resilience and hope."
        ),
    },
    "🗺️ Adventure": {
        "label": "Adventure",
        "instruction": (
            "Write in a thrilling, action-packed style with discovery, "
            "danger, and a sense of epic journey."
        ),
    },
    "🧚 Fantasy": {
        "label": "Fantasy",
        "instruction": (
            "Write in a magical, whimsical style with mythical creatures, "
            "enchanted worlds, and wonder."
        ),
    },
}
DEFAULT_STYLE = "🎭 Dramatic"

# ---------------------------------------------------------------------------
# Story lengths (target word counts)
# ---------------------------------------------------------------------------
STORY_LENGTHS: dict[str, dict] = {
    "Short (≈60 words)": {"words": 60, "label": "short"},
    "Medium (≈150 words)": {"words": 150, "label": "medium"},
    "Long (≈300 words)": {"words": 300, "label": "long"},
}
DEFAULT_LENGTH = "Medium (≈150 words)"

# ---------------------------------------------------------------------------
# Story languages
# ---------------------------------------------------------------------------
STORY_LANGUAGES: list[str] = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Hindi",
]
DEFAULT_LANGUAGE = "English"

# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------
MAX_HISTORY_ITEMS = 5

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
ALLOWED_IMAGE_TYPES = {"jpg", "jpeg", "png", "webp"}
MAX_IMAGE_SIZE_MB = 10
