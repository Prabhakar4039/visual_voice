"""
ui/sidebar.py — Sidebar controls for VisualVoice.

render_sidebar() returns a dict of all user selections so that app.py
can pass them to the service layer cleanly.
"""
from __future__ import annotations

import streamlit as st

from config import (
    DEFAULT_LANGUAGE,
    DEFAULT_LENGTH,
    DEFAULT_STYLE,
    DEFAULT_VOICE,
    STORY_LANGUAGES,
    STORY_LENGTHS,
    STORY_STYLES,
    TTS_VOICES,
)
from utils.validators import check_api_keys


def render_sidebar() -> dict[str, str]:
    """
    Render the sidebar with all generation controls.

    Returns:
        dict with keys:
          - 'style':    selected story style key
          - 'length':   selected story length key
          - 'voice':    selected TTS voice key
          - 'language': selected story language string
    """
    with st.sidebar:
        # ── Brand ──────────────────────────────────────────
        st.markdown(
            '<p class="sidebar-logo-text">✨ VisualVoice</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size:0.78rem;color:#64748b;margin-top:-0.5rem;'>AI Image-to-Story Narrator</p>",
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

        # ── Story Controls ─────────────────────────────────
        st.markdown(
            '<p class="sidebar-section-title">🎨 Story Settings</p>',
            unsafe_allow_html=True,
        )

        style_key = st.selectbox(
            "Narrative Style",
            options=list(STORY_STYLES.keys()),
            index=list(STORY_STYLES.keys()).index(DEFAULT_STYLE),
            help="Choose the emotional tone of your generated story.",
            key="sidebar_style",
        )

        length_key = st.radio(
            "Story Length",
            options=list(STORY_LENGTHS.keys()),
            index=list(STORY_LENGTHS.keys()).index(DEFAULT_LENGTH),
            help="Controls the approximate word count of the story.",
            key="sidebar_length",
        )

        language = st.selectbox(
            "Story Language",
            options=STORY_LANGUAGES,
            index=STORY_LANGUAGES.index(DEFAULT_LANGUAGE),
            help="The language in which the story will be written.",
            key="sidebar_language",
        )

        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

        # ── Voice Controls ─────────────────────────────────
        st.markdown(
            '<p class="sidebar-section-title">🎙️ Voice Settings</p>',
            unsafe_allow_html=True,
        )

        voice_key = st.selectbox(
            "Narrator Voice",
            options=list(TTS_VOICES.keys()),
            index=list(TTS_VOICES.keys()).index(DEFAULT_VOICE),
            help="Choose the AI voice for audio narration.",
            key="sidebar_voice",
        )

        # Show voice description
        voice_desc = TTS_VOICES[voice_key]["description"]
        st.markdown(
            f"<p style='font-size:0.75rem;color:#64748b;margin-top:-0.4rem;'>{voice_desc}</p>",
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

        # ── API Key Status ─────────────────────────────────
        st.markdown(
            '<p class="sidebar-section-title">🔑 API Status</p>',
            unsafe_allow_html=True,
        )

        key_statuses = check_api_keys()
        
        # Show specific dots for Groq/Grok/TTS
        for service, ok in key_statuses.items():
            dot_class = "dot-ok" if ok else "dot-err"
            label = "Connected" if ok else "Missing"
            st.markdown(
                f"""
                <div class="status-indicator">
                    <span class="{dot_class}"></span>
                    <span>{service} — {label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        # Identify active engine
        from config import GROQ_API_KEY, GROK_API_KEY
        active_provider = "None"
        if GROQ_API_KEY:
            active_provider = "Groq (High-Speed Llama)"
        elif GROK_API_KEY:
            active_provider = "Grok (xAI)"
        
        st.markdown(
            f'<p style="font-size:0.7rem;color:#94a3b8;margin-top:0.4rem;padding-left:1.5rem;">'
            f'Active Engine: <b style="color:#a855f7;">{active_provider}</b></p>',
            unsafe_allow_html=True
        )

        if not all(key_statuses.values()):
            st.warning(
                "Add missing keys to your `.env` file and restart the app.",
                icon="⚠️",
            )

        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

        # ── About ──────────────────────────────────────────
        st.markdown(
            '<p class="sidebar-section-title">ℹ️ About</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <p style='font-size:0.78rem;color:#64748b;line-height:1.65;'>
            VisualVoice uses <b>Salesforce BLIP</b> to understand images,
            <b>Groq (Llama 3.3)</b> or <b>Grok (xAI)</b> to craft compelling stories, and
            <b>HuggingFace TTS</b> to narrate them — all in one click.
            </p>
            """,
            unsafe_allow_html=True,
        )

    return {
        "style": style_key,
        "length": length_key,
        "voice": voice_key,
        "language": language,
    }
