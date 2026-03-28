# ─────────────────────────────────────────────────────────────────────────────
# VisualVoice — Dockerfile
# Production-ready container for Streamlit Cloud / Docker / Kubernetes
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Label metadata
LABEL maintainer="VisualVoice"
LABEL description="AI Image-to-Story Narrator — BLIP + Grok + HuggingFace TTS"
LABEL version="2.0.0"

# ── System dependencies ────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Non-root user for security ─────────────────────────────────────────────
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# ── Install Python dependencies ────────────────────────────────────────────
# Copy requirements first to leverage Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Copy application source ────────────────────────────────────────────────
COPY --chown=appuser:appuser . .

# Create runtime directories
RUN mkdir -p temp logs && chown -R appuser:appuser temp logs

# Switch to non-root user
USER appuser

# ── Streamlit configuration ────────────────────────────────────────────────
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_THEME_BASE=dark

# ── Health check ───────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── Expose port ────────────────────────────────────────────────────────────
EXPOSE 8501

# ── Entrypoint ─────────────────────────────────────────────────────────────
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true"]
