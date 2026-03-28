"""
ui/header.py — Branded hero header component.
"""
from __future__ import annotations

import streamlit as st


def render_header() -> None:
    """
    Render the VisualVoice branded hero header with badges.
    Uses custom HTML injected via st.markdown for full design control.
    """
    st.markdown(
        """
        <div class="fade-in-up">
            <p class="hero-title">✨ VisualVoice</p>
            <p class="hero-subtitle">
                Upload any image and watch AI transform it into a beautifully narrated story —
                powered by <strong>BLIP</strong>, <strong>Grok</strong>, and <strong>HuggingFace TTS</strong>.
            </p>
            <div class="badge-row">
                <span class="badge">🖼️ BLIP Vision</span>
                <span class="badge">⚡ Grok LLM</span>
                <span class="badge">🎙️ HF TTS</span>
                <span class="badge">🎨 7 Story Styles</span>
                <span class="badge">🌍 Multilingual</span>
                <span class="badge">📥 Download Ready</span>
            </div>
        </div>
        <hr class="fancy-divider">
        """,
        unsafe_allow_html=True,
    )
