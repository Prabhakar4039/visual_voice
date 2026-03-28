"""
ui/result_panel.py — Results display component for VisualVoice.

render_results() displays image caption, generated story, audio player,
and download buttons in a tabbed glass-card panel.
"""
from __future__ import annotations

import streamlit as st

from utils.file_helpers import build_download_zip


def render_results(
    caption: str,
    story: str,
    audio_bytes: bytes,
    settings: dict[str, str],
) -> None:
    """
    Render the full results card with tabs for caption, story, and audio.

    Args:
        caption:     Image scene description from BLIP.
        story:       Generated story from Grok LLM.
        audio_bytes: Raw audio bytes from TTS service.
        settings:    Dict with 'style', 'length', 'voice', 'language' keys.
    """
    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # ── Metrics row ───────────────────────────────────────────────────────
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("📖 Style", settings.get("style", "—").split(" ", 1)[-1])
    with col_m2:
        st.metric("📏 Length", settings.get("length", "—").split("(")[0].strip())
    with col_m3:
        st.metric("🎙️ Voice", settings.get("voice", "—").split("(")[0].strip())
    with col_m4:
        st.metric("🌍 Language", settings.get("language", "English"))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main results card ─────────────────────────────────────────────────
    st.markdown('<div class="result-card fade-in-up">', unsafe_allow_html=True)

    tab_caption, tab_story, tab_audio = st.tabs(
        ["📸 Scene Caption", "📝 Generated Story", "🎵 Audio Narration"]
    )

    # ── Caption tab ───────────────────────────────────────────────────────
    with tab_caption:
        st.markdown(
            '<p class="section-label">🔍 What the AI sees</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="caption-box">"{caption}"</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📋 Download Caption (.txt)",
            data=caption.encode("utf-8"),
            file_name="image_caption.txt",
            mime="text/plain",
            key="dl_caption",
        )

    # ── Story tab ─────────────────────────────────────────────────────────
    with tab_story:
        st.markdown(
            '<p class="section-label">✍️ AI-Generated Story</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="story-box">{story}</div>',
            unsafe_allow_html=True,
        )
        word_count = len(story.split())
        st.markdown(
            f"<p style='font-size:0.75rem;color:#64748b;margin-top:0.5rem;'>"
            f"~{word_count} words</p>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📄 Download Story (.txt)",
            data=story.encode("utf-8"),
            file_name="generated_story.txt",
            mime="text/plain",
            key="dl_story",
        )

    # ── Audio tab ─────────────────────────────────────────────────────────
    with tab_audio:
        st.markdown(
            '<p class="section-label">🎧 Listen to your story</p>',
            unsafe_allow_html=True,
        )
        st.audio(audio_bytes, format="audio/flac")
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="🎵 Download Audio (.flac)",
            data=audio_bytes,
            file_name="narrated_story.flac",
            mime="audio/flac",
            key="dl_audio",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── ZIP bundle download ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    zip_bytes = build_download_zip(audio_bytes, story, caption)
    st.download_button(
        label="📦 Download Everything (.zip)",
        data=zip_bytes,
        file_name="visualvoice_output.zip",
        mime="application/zip",
        key="dl_zip",
        help="Downloads audio, story text, and caption in a single ZIP file.",
    )


def render_history(history: list[dict]) -> None:
    """
    Render the generation history panel showing up to the last N items.

    Each history entry is a dict with: timestamp, caption, story,
    audio_bytes, style, length, voice, language, image_bytes.

    Args:
        history: List of generation result dicts (newest first).
    """
    if not history:
        return

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-label">🕒 Generation History</p>',
        unsafe_allow_html=True,
    )

    for i, item in enumerate(history):
        with st.expander(
            f"#{len(history) - i}  ·  {item['timestamp']}  ·  {item.get('style', '').split(' ', 1)[-1]}",
            expanded=False,
        ):
            col_img, col_text = st.columns([1, 2])

            with col_img:
                if item.get("image_bytes"):
                    st.image(
                        item["image_bytes"],
                        caption="Uploaded image",
                        use_container_width=True,
                    )

            with col_text:
                st.markdown(
                    f'<div class="caption-box" style="margin-bottom:0.7rem;">"{item["caption"]}"</div>',
                    unsafe_allow_html=True,
                )
                snippet = " ".join(item["story"].split()[:40]) + "…"
                st.markdown(
                    f'<div class="history-snippet">{snippet}</div>',
                    unsafe_allow_html=True,
                )

            if item.get("audio_bytes"):
                st.audio(item["audio_bytes"], format="audio/flac")

            # Per-item downloads
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    "📄 Story",
                    data=item["story"].encode("utf-8"),
                    file_name=f"story_{i+1}.txt",
                    mime="text/plain",
                    key=f"hist_story_{i}",
                )
            with dl_col2:
                if item.get("audio_bytes"):
                    st.download_button(
                        "🎵 Audio",
                        data=item["audio_bytes"],
                        file_name=f"audio_{i+1}.flac",
                        mime="audio/flac",
                        key=f"hist_audio_{i}",
                    )
