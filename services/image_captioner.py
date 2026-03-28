"""
services/image_captioner.py — BLIP image-to-text service.

The pipeline is cached using @st.cache_resource so the model is downloaded
and loaded only once per Streamlit session, even if the user uploads many
images in the same session.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import streamlit as st

from config import BLIP_MODEL_ID

logger = logging.getLogger(__name__)


@st.cache_resource(show_spinner=False)
def _load_blip_pipeline() -> Any:
    """
    Load and cache the BLIP image-to-text pipeline.

    This heavy operation runs only once thanks to @st.cache_resource.
    The cached object is shared across all Streamlit reruns.

    Returns:
        transformers.Pipeline: The loaded BLIP pipeline.

    Raises:
        RuntimeError: If the model cannot be loaded.
    """
    try:
        # Import inside function so Streamlit can cache the result object
        from transformers import pipeline  # noqa: PLC0415

        logger.info("Loading BLIP model: %s", BLIP_MODEL_ID)
        # Use device=-1 for CPU (Standard for Streamlit Cloud)
        pipe = pipeline("image-to-text", model=BLIP_MODEL_ID, device=-1)
        logger.info("BLIP model loaded successfully.")
        return pipe
    except Exception as exc:
        logger.exception("Failed to load BLIP pipeline.")
        raise RuntimeError(
            f"Could not load image captioning model ({BLIP_MODEL_ID}). "
            f"Ensure 'transformers' and 'torch' are installed.\nCause: {exc}"
        ) from exc


def caption_image(image_path: str | Path) -> str:
    """
    Generate a text caption for the given image using BLIP.

    Args:
        image_path: Absolute or relative path to the image file.

    Returns:
        A descriptive caption string produced by the BLIP model.

    Raises:
        FileNotFoundError: If the image file does not exist.
        RuntimeError: If captioning fails for any reason.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    logger.info("Captioning image: %s", path)
    try:
        pipe = _load_blip_pipeline()
        results: list[dict[str, str]] = pipe(str(path))
        caption: str = results[0]["generated_text"]
        logger.info("Caption generated: %r", caption)
        return caption.strip()
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Unexpected output format from BLIP pipeline.") from exc
    except Exception as exc:
        logger.exception("Image captioning failed.")
        raise RuntimeError(f"Image captioning failed: {exc}") from exc
