"""
services/tts_service.py — HuggingFace Inference API text-to-speech service.

Supports multiple voice models. Returns raw audio bytes so the caller
controls where the audio is written (no hardcoded file paths here).
"""

from __future__ import annotations

import logging

import requests

from config import HUGGINGFACE_API_TOKEN, TTS_VOICES

logger = logging.getLogger(__name__)

# Timeout for TTS Inference API requests (seconds)
_REQUEST_TIMEOUT = 120


def text_to_speech(text: str, voice_key: str) -> bytes:
    """
    Convert text to speech audio bytes via the HuggingFace Inference API.

    Args:
        text:      The story text to narrate.
        voice_key: Key from TTS_VOICES (e.g. '🎙️ Emma (Female, Neutral)').

    Returns:
        Raw audio content bytes (FLAC format from ESPnet, WAV from MMS-TTS).

    Raises:
        ValueError: If HuggingFace API token is missing or voice key invalid.
        RuntimeError: If the API call fails or returns an unexpected response.
    """
    if not HUGGINGFACE_API_TOKEN:
        raise ValueError(
            "HUGGINGFACE_API_TOKEN is not set. Add it to your .env file."
        )

    voice_config = TTS_VOICES.get(voice_key)
    if not voice_config:
        available = ", ".join(TTS_VOICES.keys())
        raise ValueError(
            f"Unknown voice key '{voice_key}'. Available: {available}"
        )

    api_url: str = voice_config["url"]
    headers: dict[str, str] = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload: dict[str, str] = {"inputs": text}

    logger.info("Calling TTS API | voice=%s | text_len=%d", voice_key, len(text))

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError(
            "TTS API timed out after 120 seconds. "
            "The model may be loading — please try again in a moment."
        )
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(f"Could not connect to HuggingFace API: {exc}") from exc
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "?"
        body = exc.response.text[:200] if exc.response is not None else ""
        raise RuntimeError(
            f"HuggingFace TTS API returned HTTP {status}. "
            f"Check your token and model availability.\nDetail: {body}"
        ) from exc

    audio_bytes: bytes = response.content
    if len(audio_bytes) < 100:
        raise RuntimeError(
            "TTS API returned suspiciously small audio data. "
            "The model may still be loading on HuggingFace — retry in ~30 seconds."
        )

    logger.info("Audio generated successfully (%d bytes).", len(audio_bytes))
    return audio_bytes
