"""
services/image_captioner.py — BLIP image-to-text service.

The model and processor are cached using @st.cache_resource for performance.
This refactored version uses explicit model classes for maximum stability.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import streamlit as st
from PIL import Image

from config import BLIP_MODEL_ID

logger = logging.getLogger(__name__)


@st.cache_resource(show_spinner=False)
def _load_blip_engine() -> tuple[Any, Any]:
    """
    Load and cache the BLIP model and processor.
    
    Returns:
        tuple: (model, processor) cached resources.
    """
    try:
        from transformers import BlipForConditionalGeneration, BlipProcessor  # noqa: PLC0415
        import torch  # noqa: PLC0415

        logger.info("Loading BLIP engine: %s", BLIP_MODEL_ID)
        
        processor = BlipProcessor.from_pretrained(BLIP_MODEL_ID)
        model = BlipForConditionalGeneration.from_pretrained(
            BLIP_MODEL_ID, 
            torch_dtype=torch.float32  # Standard for CPU
        ).to("cpu")
        
        logger.info("BLIP engine loaded successfully.")
        return model, processor
    except Exception as exc:
        logger.exception("Failed to load BLIP engine.")
        raise RuntimeError(f"Could not load image captioning engine: {exc}") from exc


def caption_image(image_path: str | Path) -> str:
    """
    Generate a text caption for an image using BLIP (Explicit Mode).
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    logger.info("Captioning image: %s", path)
    try:
        model, processor = _load_blip_engine()
        
        # Load and convert image to RGB (Standard for BLIP)
        raw_image = Image.open(path).convert("RGB")
        
        # Process and generate
        inputs = processor(images=raw_image, return_tensors="pt")
        
        import torch  # noqa: PLC0415
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=50)
            
        caption: str = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        
        logger.info("Caption generated: %r", caption)
        return caption.strip()
    except Exception as exc:
        logger.exception("Image captioning failed.")
        raise RuntimeError(f"Image captioning failed: {exc}") from exc
