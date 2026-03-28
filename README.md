# ✨ VisualVoice — AI Image-to-Story Narrator

> Upload any image. Get a beautifully narrated story back — in seconds.

**VisualVoice** is a production-grade Streamlit application that chains three AI models:
1. 🖼️ **Salesforce BLIP** — Understands what's in your image
2. ⚡ **Grok (xAI)** — Crafts a story in your chosen style & language
3. 🎙️ **HuggingFace TTS** — Narrates it with a natural AI voice

---

## 🚀 Features

| Feature | Details |
|---|---|
| 🎨 **7 Story Styles** | Dramatic, Funny, Horror, Romantic, Motivational, Adventure, Fantasy |
| 📏 **3 Story Lengths** | Short (~60w), Medium (~150w), Long (~300w) |
| 🎙️ **Voice Selection** | Emma, Ryan, Jenny, Alex — multiple HuggingFace TTS voices |
| 🌍 **7 Languages** | English, Spanish, French, German, Italian, Portuguese, Hindi |
| 📥 **Download Options** | Audio (.flac), Story (.txt), Caption (.txt), Bundle (.zip) |
| 🕒 **History** | Last 5 generations with thumbnail, audio replay & per-item downloads |
| 🔑 **API Status** | Live sidebar indicators show which keys are connected |
| 🛡️ **Error Handling** | Graceful degradation — shows story even if TTS fails |
| ⚡ **Model Caching** | BLIP loads once per session (`@st.cache_resource`) |
| 🐳 **Docker Ready** | Production Dockerfile with healthcheck & non-root user |

---

## 📁 Project Structure

```
visualvoice/
├── app.py                  # Entry point — slim orchestrator
├── config.py               # All constants, prompts, model names
├── requirements.txt        # Pinned dependencies
├── .env.example            # Secret key template
├── Dockerfile              # Production container
├── .dockerignore
│
├── services/               # AI logic layer
│   ├── image_captioner.py  # BLIP image-to-text (cached)
│   ├── story_generator.py  # Grok API story generation
│   └── tts_service.py      # HuggingFace TTS
│
├── utils/                  # Shared helpers
│   ├── custom.py           # Dark SaaS CSS theme
│   ├── validators.py       # Input validation
│   ├── file_helpers.py     # File I/O, ZIP bundler
│   └── logger.py           # Structured logging
│
└── ui/                     # Streamlit UI components
    ├── header.py           # Branded hero header
    ├── sidebar.py          # Controls sidebar
    └── result_panel.py     # Results + history display
```

---

## ⚙️ Setup

### 1. Clone & install

```bash
git clone https://github.com/your-repo/visualvoice.git
cd visualvoice
pip install -r requirements.txt
```

### 2. Set API keys

```bash
cp .env.example .env
```

Edit `.env`:
```env
HUGGINGFACE_API_TOKEN=hf_your_token_here   # https://huggingface.co/settings/tokens
GROK_API_KEY=xai_your_key_here             # https://console.x.ai/
```

### 3. Run locally

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🐳 Docker Deployment

```bash
# Build
docker build -t visualvoice:latest .

# Run (pass secrets via env flags or a .env file)
docker run -p 8501:8501 \
  -e HUGGINGFACE_API_TOKEN=hf_xxx \
  -e GROK_API_KEY=xai_xxx \
  visualvoice:latest
```

---

## ☁️ Streamlit Cloud Deployment

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select `app.py` as the entry point
4. Add `HUGGINGFACE_API_TOKEN` and `GROK_API_KEY` under **Secrets**
5. Deploy 🎉

---

## 🔧 Configuration

All behaviour is controlled via `config.py` — no magic strings scattered across files:

| Config | Key | Default |
|---|---|---|
| LLM Model | `GROK_MODEL` | `grok-2-1212` |
| BLIP Model | `BLIP_MODEL_ID` | `Salesforce/blip-image-captioning-base` |
| Default Voice | `DEFAULT_VOICE` | `🎙️ Emma (Female, Neutral)` |
| Default Style | `DEFAULT_STYLE` | `🎭 Dramatic` |
| Max History | `MAX_HISTORY_ITEMS` | `5` |
| Max Image Size | `MAX_IMAGE_SIZE_MB` | `10` |
| LLM Retries | `GROK_MAX_RETRIES` | `3` |

---

## 📊 Architecture

```
Upload Image
     │
     ▼
services/image_captioner.py  ──  BLIP (cached, local)
     │  caption text
     ▼
services/story_generator.py  ──  Grok API (xAI)
     │  story text
     ▼
services/tts_service.py      ──  HuggingFace Inference API
     │  audio bytes
     ▼
ui/result_panel.py           ──  Tabs + Downloads + History
```

---

## 🛡️ Error Handling Strategy

| Failure | Behaviour |
|---|---|
| Missing API key | Sidebar shows red dot + warning banner |
| Invalid image type/size | Immediate `st.error` before any processing |
| BLIP load failure | Clear error with install instructions |
| Grok API rate limit | Auto-retry with exponential backoff (up to 3×) |
| Grok API 4xx/5xx | Specific error with HTTP code shown |
| TTS failure | **Degraded mode** — shows story text + download, skips audio |
| TTS timeout | User-friendly "model loading" message with retry hint |

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.
