"""
utils/validators.py — Input validation helpers for the Streamlit app.
"""

from __future__ import annotations

import logging
from typing import Any

from config import ALLOWED_IMAGE_TYPES, GROK_API_KEY, GROQ_API_KEY, HUGGINGFACE_API_TOKEN, MAX_IMAGE_SIZE_MB

logger = logging.getLogger(__name__)


def validate_image(uploaded_file: Any) -> tuple[bool, str]:
    """
    Validate an uploaded file from st.file_uploader.

    Checks:
    - File is not None
    - Extension is in ALLOWED_IMAGE_TYPES
    - File size does not exceed MAX_IMAGE_SIZE_MB

    Args:
        uploaded_file: The UploadedFile object from st.file_uploader.

    Returns:
        (True, "") if valid, or (False, "<reason>") if invalid.
    """
    if uploaded_file is None:
        return False, "No file uploaded."

    filename: str = uploaded_file.name or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_IMAGE_TYPES:
        return False, (
            f"Unsupported file type '.{ext}'. "
            f"Please upload one of: {', '.join(sorted(ALLOWED_IMAGE_TYPES))}."
        )

    # getvalue() returns bytes; check size
    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        return False, (
            f"File is too large ({size_mb:.1f} MB). "
            f"Maximum allowed size is {MAX_IMAGE_SIZE_MB} MB."
        )

    return True, ""


def check_api_keys() -> dict[str, bool]:
    """
    Check whether required API keys are present in the environment.

    Returns:
        Dict mapping service name to bool (True = key present and non-empty).
    """
    return {
        "HuggingFace (TTS)": bool(HUGGINGFACE_API_TOKEN),
        "Groq (Story)": bool(GROQ_API_KEY),
        "Grok (Story)": bool(GROK_API_KEY),
    }
