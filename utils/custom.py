"""
utils/custom.py — Full dark SaaS CSS theme for VisualVoice.

Injected via st.markdown(..., unsafe_allow_html=True) in app.py.
Uses Inter font from Google Fonts, custom color palette, glassmorphism
cards, gradient accents, and micro-animations.
"""

CSS: str = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
/* ─────────────────────────────────────────
   ROOT VARIABLES — design tokens
───────────────────────────────────────── */
:root {
    --bg-primary:    #0d0f1a;
    --bg-secondary:  #13162a;
    --bg-card:       rgba(255,255,255,0.04);
    --bg-card-hover: rgba(255,255,255,0.07);
    --accent-1:      #7c3aed;
    --accent-2:      #a855f7;
    --accent-3:      #06b6d4;
    --gradient:      linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #06b6d4 100%);
    --gradient-soft: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(6,182,212,0.10) 100%);
    --text-primary:  #f1f5f9;
    --text-secondary:#94a3b8;
    --text-muted:    #64748b;
    --border:        rgba(255,255,255,0.08);
    --border-accent: rgba(124,58,237,0.4);
    --success:       #10b981;
    --error:         #ef4444;
    --warning:       #f59e0b;
    --radius-sm:     8px;
    --radius-md:     14px;
    --radius-lg:     20px;
    --shadow-card:   0 4px 32px rgba(0,0,0,0.4);
    --shadow-glow:   0 0 40px rgba(124,58,237,0.25);
}

/* ─────────────────────────────────────────
   GLOBAL RESET & BASE
───────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: var(--bg-primary) !important;
}

/* Hide Streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px !important;
}

/* ─────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem !important;
}

.sidebar-logo-text {
    font-size: 1.4rem;
    font-weight: 800;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}

.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin: 1.2rem 0 0.5rem 0;
}

/* ─────────────────────────────────────────
   HEADINGS & TEXT
───────────────────────────────────────── */
h1, h2, h3, h4 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    letter-spacing: -1.5px;
    margin-bottom: 0.25rem;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary) !important;
    font-weight: 400;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

/* ─────────────────────────────────────────
   BADGE ROW
───────────────────────────────────────── */
.badge-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 2rem; }

.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    border: 1px solid var(--border-accent);
    background: rgba(124,58,237,0.1);
    color: var(--accent-2) !important;
}

/* ─────────────────────────────────────────
   CARDS / GLASS PANELS
───────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    box-shadow: var(--shadow-card);
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
    backdrop-filter: blur(12px);
}

.glass-card:hover {
    border-color: var(--border-accent);
    box-shadow: var(--shadow-glow);
}

.result-card {
    background: var(--gradient-soft);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius-lg);
    padding: 1.75rem 2rem;
    margin-top: 1rem;
    box-shadow: var(--shadow-glow);
}

.caption-box {
    background: rgba(6,182,212,0.07);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
    color: var(--text-secondary) !important;
    font-size: 0.95rem;
    font-style: italic;
    line-height: 1.7;
}

.story-box {
    background: rgba(124,58,237,0.06);
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: var(--radius-md);
    padding: 1.25rem 1.5rem;
    font-size: 1rem;
    line-height: 1.85;
    color: var(--text-primary) !important;
    white-space: pre-wrap;
}

/* ─────────────────────────────────────────
   SECTION LABELS
───────────────────────────────────────── */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--accent-2) !important;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 8px;
}

/* ─────────────────────────────────────────
   BUTTONS
───────────────────────────────────────── */
.stButton > button {
    background: var(--gradient) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 2px 16px rgba(124,58,237,0.35) !important;
    letter-spacing: 0.2px;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(124,58,237,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Download buttons — secondary style */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent-2) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: background 0.2s ease, color 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(124,58,237,0.15) !important;
    color: var(--text-primary) !important;
}

/* ─────────────────────────────────────────
   FILE UPLOADER
───────────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--border-accent) !important;
    border-radius: var(--radius-lg) !important;
    background: var(--bg-card) !important;
    transition: border-color 0.25s;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-2) !important;
    background: var(--bg-card-hover) !important;
}

/* ─────────────────────────────────────────
   SELECTBOX / RADIO
───────────────────────────────────────── */
.stSelectbox > div > div,
.stRadio > div {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

/* ─────────────────────────────────────────
   TABS
───────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.5rem 1.1rem !important;
    transition: color 0.2s, background 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(124,58,237,0.12) !important;
    color: var(--accent-2) !important;
    border-bottom: 2px solid var(--accent-2) !important;
}

/* ─────────────────────────────────────────
   HISTORY CARD
───────────────────────────────────────── */
.history-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s, transform 0.2s;
    cursor: default;
}
.history-card:hover {
    border-color: var(--border-accent);
    transform: translateX(3px);
}
.history-meta {
    font-size: 0.72rem;
    color: var(--text-muted) !important;
    margin-bottom: 0.3rem;
}
.history-snippet {
    font-size: 0.88rem;
    color: var(--text-secondary) !important;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ─────────────────────────────────────────
   STATUS DOTS (API Keys)
───────────────────────────────────────── */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-secondary) !important;
    padding: 4px 0;
}
.dot-ok  { width: 8px; height: 8px; border-radius: 50%; background: var(--success); box-shadow: 0 0 6px var(--success); display: inline-block; }
.dot-err { width: 8px; height: 8px; border-radius: 50%; background: var(--error);   box-shadow: 0 0 6px var(--error);   display: inline-block; }

/* ─────────────────────────────────────────
   DIVIDER
───────────────────────────────────────── */
.fancy-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-accent), transparent);
    margin: 2rem 0;
    border: none;
}

/* ─────────────────────────────────────────
   SPINNER OVERRIDE
───────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--accent-1) !important;
}

/* ─────────────────────────────────────────
   AUDIO PLAYER
───────────────────────────────────────── */
audio {
    width: 100% !important;
    border-radius: var(--radius-sm) !important;
    outline: none;
    filter: drop-shadow(0 2px 12px rgba(124,58,237,0.25));
}

/* ─────────────────────────────────────────
   EXPANDER
───────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ─────────────────────────────────────────
   METRICS
───────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 1rem 1.25rem !important;
}
[data-testid="stMetricValue"] { color: var(--accent-2) !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }

/* ─────────────────────────────────────────
   SCROLLBAR
───────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-accent); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-1); }

/* ─────────────────────────────────────────
   PULSE ANIMATION (used on loading)
───────────────────────────────────────── */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(124,58,237,0.2); }
    50%       { box-shadow: 0 0 40px rgba(124,58,237,0.5); }
}
.pulsing { animation: pulse-glow 2s ease-in-out infinite; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in-up { animation: fadeInUp 0.5s ease forwards; }
</style>
"""