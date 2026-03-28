"""
app.py — VisualVoice: AI Image-to-Story Narrator
─────────────────────────────────────────────────
Entry point and slim orchestrator. All heavy logic lives in services/.
This file only:
  1. Configures Streamlit page settings
  2. Initialises session state and logging
  3. Renders UI components (header, sidebar, upload, results, history)
  4. Calls service functions and handles errors
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import streamlit as st

from config import LOGS_DIR, MAX_HISTORY_ITEMS
from services.image_captioner import caption_image
from services.story_generator import generate_story
from services.tts_service import text_to_speech
from ui.header import render_header
from ui.result_panel import render_history, render_results
from ui.sidebar import render_sidebar
from utils.custom import CSS
from utils.file_helpers import save_uploaded_image
from utils.logger import setup_logging
from utils.validators import validate_image

# ── Logging ───────────────────────────────────────────────────────────────
setup_logging(log_dir=LOGS_DIR)
logger = logging.getLogger(__name__)

# ── Page config (must be first Streamlit call) ────────────────────────────
st.set_page_config(
    page_title="VisualVoice — AI Image-to-Story Narrator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/",
        "Report a bug": "https://github.com/",
        "About": "VisualVoice — powered by BLIP, Grok, and HuggingFace TTS.",
    },
)

# ── Inject CSS theme ──────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)


# ── Session state initialisation ──────────────────────────────────────────
def _init_session_state() -> None:
    """Initialise all required session state keys on first run."""
    defaults: dict = {
        "history": [],           # list of generation result dicts
        "last_result": None,     # most recent generation (or None)
        "processing": False,     # guard against duplicate submissions
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _add_to_history(
    caption: str,
    story: str,
    audio_bytes: bytes,
    image_bytes: bytes,
    settings: dict[str, str],
) -> None:
    """
    Prepend the latest generation to session history, capped at MAX_HISTORY_ITEMS.

    Args:
        caption:     BLIP-generated scene description.
        story:       Grok-generated story.
        audio_bytes: Raw audio bytes from TTS.
        image_bytes: Raw bytes of the original uploaded image.
        settings:    Dict of style/length/voice/language selections.
    """
    entry = {
        "timestamp": datetime.now().strftime("%b %d, %H:%M"),
        "caption": caption,
        "story": story,
        "audio_bytes": audio_bytes,
        "image_bytes": image_bytes,
        **settings,
    }
    st.session_state.history.insert(0, entry)
    st.session_state.history = st.session_state.history[:MAX_HISTORY_ITEMS]


# ── Main application ──────────────────────────────────────────────────────
def main() -> None:
    """Main Streamlit application entry point."""
    _init_session_state()

    # Sidebar — renders controls and returns user selections
    settings = render_sidebar()

    # Header — hero section with badges
    render_header()

    # ── Upload section ────────────────────────────────────────────────────
    st.markdown(
        '<p class="section-label">📤 Upload Your Image</p>',
        unsafe_allow_html=True,
    )

    upload_col, info_col = st.columns([3, 2], gap="large")

    with upload_col:
        uploaded_file = st.file_uploader(
            label="Drop an image here, or click to browse",
            type=["jpg", "jpeg", "png", "webp"],
            help=(
                f"Supported: JPG, JPEG, PNG, WEBP · Max 10 MB\n\n"
                "The AI will analyse your image, craft a story, and narrate it."
            ),
            key="image_uploader",
            label_visibility="collapsed",
        )

    with info_col:
        st.markdown(
            """
            <div class="glass-card">
                <p style="font-size:0.8rem;color:#94a3b8;margin:0;line-height:1.8;">
                <b style="color:#a855f7;">How it works:</b><br>
                1️⃣ &nbsp;Upload any image (photo, illustration, etc.)<br>
                2️⃣ &nbsp;AI reads the scene with <b>BLIP Vision</b><br>
                3️⃣ &nbsp;Grok crafts your story in the chosen style<br>
                4️⃣ &nbsp;HuggingFace TTS narrates it in your voice<br>
                5️⃣ &nbsp;Download audio + text in one click
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Validation ────────────────────────────────────────────────────────
    if uploaded_file is not None:
        valid, error_msg = validate_image(uploaded_file)
        if not valid:
            st.error(f"❌ {error_msg}", icon="🚫")
            return

        # Show uploaded image preview
        st.markdown("<br>", unsafe_allow_html=True)
        prev_col, _ = st.columns([2, 3])
        with prev_col:
            st.image(
                uploaded_file,
                caption="Your uploaded image",
                use_container_width=True,
            )

        # ── Generate button ───────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)

        # Reset stuck processing flag if user uploads a new file
        if st.session_state.get("_last_uploaded") != uploaded_file.name:
            st.session_state["_last_uploaded"] = uploaded_file.name
            st.session_state.processing = False
            st.session_state.last_result = None

        generate_clicked = st.button(
            "✨ Generate Story & Narration",
            key="btn_generate",
            use_container_width=False,
            disabled=st.session_state.processing,
        )

        # Results placeholder — renders inline below the button
        result_area = st.container()

        if generate_clicked:
            st.session_state.processing = True
            image_bytes = uploaded_file.getvalue()

            with result_area:
                # Single st.status() block — shows live step progress inline,
                # persists as a collapsed "Complete" card when done.
                with st.status(
                    "⚙️ Generating your story…", expanded=True
                ) as status:

                    # Step 1 — Save image
                    st.write("💾 Saving uploaded image…")
                    try:
                        saved_path = save_uploaded_image(uploaded_file)
                    except Exception as exc:
                        status.update(label="❌ Failed to save image", state="error")
                        st.error(str(exc))
                        logger.exception("Image save failed.")
                        st.session_state.processing = False
                        return

                    # Step 2 — BLIP captioning
                    st.write("🔍 Analysing image with BLIP Vision…")
                    st.caption(
                        "_First run downloads the BLIP model (~500 MB) — "
                        "this may take a few minutes. Subsequent runs are instant._"
                    )
                    caption: str = ""
                    try:
                        caption = caption_image(saved_path)
                        logger.info("Caption: %r", caption)
                        st.write(f"✅ Scene understood: _{caption}_")
                    except Exception as exc:
                        status.update(label="❌ Image analysis failed", state="error")
                        st.error(
                            f"Image analysis failed: {exc}\n\n"
                            "Make sure `transformers` and `torch` are installed."
                        )
                        logger.exception("Captioning failed.")
                        st.session_state.processing = False
                        return

                    # Step 3 — Story generation
                    style_label = settings["style"].split(" ", 1)[-1]
                    st.write(f"✍️ Crafting a **{style_label}** story with Grok…")
                    story: str = ""
                    try:
                        story = generate_story(
                            caption=caption,
                            style_key=settings["style"],
                            length_key=settings["length"],
                            language=settings["language"],
                        )
                        logger.info("Story: %d words", len(story.split()))
                        st.write(f"✅ Story generated ({len(story.split())} words)")
                    except ValueError as exc:
                        status.update(label="❌ Configuration error", state="error")
                        st.error(f"Missing API key: {exc}")
                        logger.error("Story config error: %s", exc)
                        st.session_state.processing = False
                        return
                    except Exception as exc:
                        status.update(label="❌ Story generation failed", state="error")
                        st.error(
                            f"Story generation failed: {exc}\n\n"
                            "Check your GROK_API_KEY and network connection."
                        )
                        logger.exception("Story generation failed.")
                        st.session_state.processing = False
                        return

                    # Step 4 — TTS narration
                    voice_label = settings["voice"].split("(")[0].strip()
                    st.write(f"🎙️ Narrating with **{voice_label}**…")
                    audio_bytes: bytes = b""
                    try:
                        audio_bytes = text_to_speech(
                            text=story,
                            voice_key=settings["voice"],
                        )
                        st.write("✅ Audio narration ready")
                    except ValueError as exc:
                        status.update(label="❌ Configuration error", state="error")
                        st.error(f"Missing API key: {exc}")
                        logger.error("TTS config error: %s", exc)
                        st.session_state.processing = False
                        return
                    except Exception as exc:
                        st.warning(
                            f"⚠️ Audio narration failed (continuing without audio): {exc}"
                        )
                        logger.warning("TTS failed: %s", exc)

                    status.update(
                        label="✅ Your story is ready!", state="complete", expanded=False
                    )

                # Store result in session state
                st.session_state.last_result = {
                    "caption": caption,
                    "story": story,
                    "audio_bytes": audio_bytes,
                    "image_bytes": image_bytes,
                    "settings": settings,
                }
                _add_to_history(caption, story, audio_bytes, image_bytes, settings)
                st.session_state.processing = False

                # Render results inline — no rerun needed
                if audio_bytes:
                    render_results(
                        caption=caption,
                        story=story,
                        audio_bytes=audio_bytes,
                        settings=settings,
                    )
                else:
                    # Degraded mode — no audio
                    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="caption-box">"{caption}"</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="story-box">{story}</div>',
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        "📄 Download Story",
                        data=story.encode("utf-8"),
                        file_name="generated_story.txt",
                        mime="text/plain",
                    )

        # ── Display result from previous generation (on fresh load) ──────
        elif st.session_state.last_result is not None:
            res = st.session_state.last_result
            with result_area:
                if res["audio_bytes"]:
                    render_results(
                        caption=res["caption"],
                        story=res["story"],
                        audio_bytes=res["audio_bytes"],
                        settings=res["settings"],
                    )
                else:
                    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="caption-box">"{res["caption"]}"</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="story-box">{res["story"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        "📄 Download Story",
                        data=res["story"].encode("utf-8"),
                        file_name="generated_story.txt",
                        mime="text/plain",
                    )

    # ── History panel ─────────────────────────────────────────────────────
    if st.session_state.history:
        render_history(st.session_state.history)


if __name__ == "__main__":
    main()