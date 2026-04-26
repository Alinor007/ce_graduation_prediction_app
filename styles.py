"""
styles.py
Pure data: design-system CSS and all HTML template strings.
Nothing here imports streamlit or does any logic.
"""

import base64 as _b64
import pathlib as _pl

def _logo_b64() -> str:
    p = _pl.Path(__file__).parent / 'pictures' / 'logo' / 'logo.png'
    return _b64.b64encode(p.read_bytes()).decode()

_LOGO_B64 = _logo_b64()
LOGO_IMG_TAG = f'<img src="data:image/png;base64,{_LOGO_B64}" style="width:38px;height:38px;object-fit:contain;" />'

# ── Philippine Grading Scale ───────────────────────────────────
PH_GRADE_OPTIONS = [None, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 2.75, 3.0, 5.0]
PH_GRADE_LABELS = {
    None: "— Not taken —",
    1.0:  "1.0 ",
    1.25: "1.25",
    1.5:  "1.5 ",
    1.75: "1.75",
    2.0:  "2.0",
    2.5:  "2.5",
    2.75: "2.75",
    3.0:  "3.0",
    5.0:  "5.0 ",
}


# ═══════════════════════════════════════════════════════════════
#  CSS — Complete Design System
# ═══════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

/* ── Design Tokens ─────────────────────────────────────────── */
:root {
  --maroon:        #9d1c20;
  --maroon-dk:     #7a1518;
  --maroon-deep:   #500c0f;
  --maroon-lt:     #c42328;
  --maroon-pale:   rgba(157, 28, 32, 0.07);
  --maroon-glow:   rgba(157, 28, 32, 0.22);

  --gold:          #f4d03f;
  --gold-dk:       #c9a80c;
  --gold-lt:       #f9e67a;
  --gold-pale:     rgba(244, 208, 63, 0.10);

  --white:         #ffffff;
  --canvas:        #f6f5f3;
  --surface:       #ffffff;
  --surface-2:     #f9f8f7;

  --text:          #1c1917;
  --text-2:        #44403c;
  --text-3:        #78716c;
  --text-4:        #a8a29e;

  --border:        #e7e5e3;
  --border-lt:     #f0eeed;

  --sh-xs:  0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.03);
  --sh-sm:  0 2px 6px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
  --sh-md:  0 4px 18px rgba(0,0,0,0.08), 0 2px 6px rgba(0,0,0,0.04);
  --sh-lg:  0 8px 38px rgba(157,28,32,0.13), 0 3px 10px rgba(0,0,0,0.05);
  --sh-xl:  0 16px 56px rgba(157,28,32,0.19), 0 6px 18px rgba(0,0,0,0.07);

  --r-xs: 6px;
  --r-sm: 10px;
  --r-md: 14px;
  --r-lg: 20px;
  --r-xl: 28px;

  --nav-h: 64px;

  --font-display: 'Cormorant Garamond', Georgia, serif;
  --font-body:    'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Base ──────────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: var(--font-body);
  color: var(--text);
}

#MainMenu { display: none; }
footer    { visibility: hidden; }
header    { visibility: hidden; height: 0 !important; min-height: 0 !important; }

.stApp {
  background: var(--canvas);
}

/* Push main content below fixed navbar */
section.main .block-container {
  padding-top: calc(var(--nav-h) + 2rem) !important;
  max-width: 1200px !important;
}

/* Sidebar top spacing */
[data-testid="stSidebar"] > div:first-child {
  padding-top: calc(var(--nav-h) + 1rem) !important;
}

/* ── Fixed Navbar ──────────────────────────────────────────── */
.ce-navbar {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 999999 !important;
  height: var(--nav-h);
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1.5px solid var(--border);
  display: flex !important;
  align-items: center;
  padding: 0 32px;
  gap: 0;
  box-shadow: 0 1px 0 var(--border), 0 2px 12px rgba(0,0,0,0.04);
  transition: box-shadow 0.2s;
}

.ce-nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  text-decoration: none;
  cursor: default;
}

.ce-nav-logo-mark {
  width: 38px;
  height: 38px;
  background: none;
  border-radius: var(--r-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.ce-nav-logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.ce-nav-logo-main {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.01em;
}

.ce-nav-logo-main em {
  color: var(--maroon);
  font-style: normal;
}

.ce-nav-logo-sub {
  font-size: 0.65rem;
  font-weight: 500;
  color: var(--text-4);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-top: 2px;
}

.ce-nav-sep {
  width: 1px;
  height: 26px;
  background: var(--border);
  margin: 0 24px;
  flex-shrink: 0;
}

.ce-nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.ce-nav-link {
  display: inline-flex;
  align-items: center;
  padding: 7px 15px;
  border-radius: var(--r-sm);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-3);
  text-decoration: none;
  cursor: pointer;
  border: none;
  background: transparent;
  transition: background 0.15s ease, color 0.15s ease;
  letter-spacing: 0.01em;
  font-family: var(--font-body);
}

.ce-nav-link:hover {
  background: var(--maroon-pale);
  color: var(--maroon);
}

.ce-nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
  flex-shrink: 0;
}

.ce-nav-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 6px 14px;
  background: var(--maroon);
  color: white;
  font-size: 0.70rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  border-radius: 100px;
  line-height: 1;
}

.ce-nav-pill-dot {
  width: 6px;
  height: 6px;
  background: var(--gold);
  border-radius: 50%;
  flex-shrink: 0;
  animation: dotPulse 2.5s ease-in-out infinite;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.55; transform: scale(0.7); }
}

@media (max-width: 768px) {
  .ce-nav-links { display: none; }
  .ce-nav-sep   { display: none; }
  .ce-navbar    { padding: 0 16px; }
  .ce-nav-pill  { display: none; }
  .ce-nav-logo-sub { display: none; }
}

/* ── Hero ──────────────────────────────────────────────────── */
.ce-hero {
  background: linear-gradient(135deg, var(--maroon-deep) 0%, var(--maroon) 48%, var(--maroon-lt) 100%);
  border-radius: var(--r-xl);
  padding: 52px 56px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  box-shadow: var(--sh-xl);
  animation: heroIn 0.65s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes heroIn {
  from { opacity: 0; transform: translateY(-14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.ce-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
  background-size: 36px 36px;
  pointer-events: none;
}

.ce-hero::after {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(244,208,63,0.14) 0%, transparent 65%);
  pointer-events: none;
}

.ce-hero-content {
  position: relative;
  z-index: 1;
  flex: 1;
  max-width: 580px;
}

.ce-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(244, 208, 63, 0.14);
  border: 1px solid rgba(244, 208, 63, 0.32);
  color: var(--gold-lt);
  font-size: 0.70rem;
  font-weight: 700;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  padding: 5px 14px 5px 10px;
  border-radius: 100px;
  margin-bottom: 20px;
  animation: heroIn 0.65s 0.1s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ce-badge-dot {
  width: 6px;
  height: 6px;
  background: var(--gold);
  border-radius: 50%;
  animation: dotPulse 2.5s ease-in-out infinite;
  flex-shrink: 0;
}

.ce-hero-title {
  font-family: var(--font-display);
  font-size: 3.4rem;
  font-weight: 700;
   color: #ffffff !important;
  margin: 0 0 14px;
  line-height: 1.08;
  letter-spacing: -0.025em;
  animation: heroIn 0.65s 0.15s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ce-hero-accent {
  color: var(--gold);
  display: block;
}

.ce-hero-sub {
  font-size: 0.98rem;
  color: rgba(255, 255, 255, 0.68);
  margin: 0 0 30px;
  line-height: 1.7;
  max-width: 430px;
  animation: heroIn 0.65s 0.2s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ce-hero-stats {
  display: flex;
  gap: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.10);
  animation: heroIn 0.65s 0.25s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ce-hero-stat { display: flex; flex-direction: column; gap: 3px; }

.ce-stat-num {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--gold);
  line-height: 1;
}

.ce-stat-lbl {
  font-size: 0.68rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.48);
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.ce-hero-visual {
  position: relative;
  z-index: 1;
  flex-shrink: 0;
  width: 220px;
  height: 220px;
  animation: heroIn 0.65s 0.2s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@media (max-width: 960px) {
  .ce-hero          { padding: 40px 36px; }
  .ce-hero-title    { font-size: 2.6rem; }
  .ce-hero-visual   { display: none; }
}

@media (max-width: 640px) {
  .ce-hero          { padding: 32px 24px; border-radius: var(--r-lg); }
  .ce-hero-title    { font-size: 2.1rem; }
  .ce-hero-stats    { gap: 20px; }
}

/* ── Model Overview Cards ──────────────────────────────────── */
.ce-models-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-bottom: 28px;
  animation: fadeUp 0.5s 0.1s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ce-model-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 22px 20px;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  position: relative;
  overflow: hidden;
}

.ce-model-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--maroon), var(--maroon-lt));
  opacity: 0;
  transition: opacity 0.18s;
}

.ce-model-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--sh-lg);
  border-color: transparent;
}

.ce-model-card:hover::before { opacity: 1; }

.ce-model-num {
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 700;
  color: rgba(157,28,32,0.12);
  line-height: 1;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.ce-model-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text);
  margin-bottom: 5px;
}

.ce-model-desc {
  font-size: 0.80rem;
  color: var(--text-3);
  line-height: 1.5;
  margin-bottom: 12px;
}

.ce-model-tag {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  background: var(--maroon-pale);
  color: var(--maroon);
  font-size: 0.70rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border-radius: 100px;
}

@media (max-width: 760px) {
  .ce-models-row { grid-template-columns: 1fr; }
}

/* ── Section Cards ─────────────────────────────────────────── */
.ce-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 24px 28px;
  margin-bottom: 16px;
  box-shadow: var(--sh-sm);
  transition: box-shadow 0.2s ease;
  animation: fadeUp 0.42s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ce-card:hover { box-shadow: var(--sh-md); }

.ce-card-hd {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 14px;
  margin-bottom: 18px;
  border-bottom: 1px solid var(--border-lt);
}

.ce-card-icon {
  width: 30px;
  height: 30px;
  background: var(--maroon-pale);
  border-radius: var(--r-xs);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.ce-card-title {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: var(--maroon);
}

/* ── Note Banner ───────────────────────────────────────────── */
.ce-note {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: #fffceb;
  border: 1px solid rgba(244, 208, 63, 0.32);
  border-left: 3px solid var(--gold-dk);
  border-radius: 0 var(--r-sm) var(--r-sm) 0;
  padding: 10px 14px;
  margin-bottom: 16px;
  font-size: 0.83rem;
  color: #7c5600;
  line-height: 1.55;
}

/* ── SASE Total ────────────────────────────────────────────── */
.ce-sase-total {
  background: linear-gradient(135deg, var(--maroon) 0%, var(--maroon-dk) 100%);
  border-radius: var(--r-md);
  padding: 20px 24px;
  margin: 14px 0;
  text-align: center;
  box-shadow: 0 4px 20px var(--maroon-glow);
  position: relative;
  overflow: hidden;
}

.ce-sase-total::after {
  content: '';
  position: absolute;
  top: -30px; right: -30px;
  width: 100px; height: 100px;
  background: radial-gradient(circle, rgba(244,208,63,0.18) 0%, transparent 70%);
  pointer-events: none;
}

.ce-sase-lbl {
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(249, 230, 122, 0.85);
  margin-bottom: 6px;
}

.ce-sase-val {
  font-family: var(--font-display);
  font-size: 3rem;
  font-weight: 700;
  color: white;
  line-height: 1;
  margin-bottom: 6px;
}

.ce-sase-bk {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.52);
}

/* ── Predict Button ────────────────────────────────────────── */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, var(--maroon) 0%, var(--maroon-dk) 100%) !important;
  color: white !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  font-family: var(--font-body) !important;
  border: none !important;
  border-radius: var(--r-md) !important;
  padding: 14px 24px !important;
  width: 100% !important;
  cursor: pointer !important;
  box-shadow: 0 4px 16px var(--maroon-glow) !important;
  transition: transform 0.15s ease, box-shadow 0.15s ease !important;
  letter-spacing: 0.025em !important;
}

div[data-testid="stButton"] > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px var(--maroon-glow) !important;
}

div[data-testid="stButton"] > button:active {
  transform: translateY(0) !important;
}

/* ── Tab Bar ───────────────────────────────────────────────── */
[data-testid="stTabs"] { margin-top: 4px; }

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: var(--surface-2) !important;
  border-radius: var(--r-md) !important;
  padding: 4px !important;
  gap: 3px !important;
  border: 1px solid var(--border) !important;
  margin-bottom: 24px;
  overflow-x: auto;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
  border-radius: var(--r-sm) !important;
  font-weight: 500 !important;
  font-size: 0.875rem !important;
  border: none !important;
  background: transparent !important;
  color: var(--text-3) !important;
  padding: 9px 18px !important;
  transition: background 0.15s, color 0.15s !important;
  flex: 1 !important;
  justify-content: center !important;
  white-space: nowrap !important;
  font-family: var(--font-body) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  background: var(--maroon-pale) !important;
  color: var(--maroon) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
  background: var(--maroon) !important;
  color: white !important;
  font-weight: 600 !important;
  box-shadow: var(--sh-xs) !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] {
  display: none !important;
}

/* ── Sidebar ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #1c0e0f 0%, #2e1415 45%, #3d1518 100%) !important;
  border-right: none !important;
}

[data-testid="stSidebar"] * { color: #f0ebe9 !important; }

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--gold) !important; }

/* Selectbox container — white bg so selected text is readable */
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
  background:var(--maroon)!important;
  border-color: var(--maroon) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="input-container"],
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="valueContainer"],
[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="single-value"],
[data-testid="stSidebar"] [data-baseweb="select"] input {
  color: #1c0e0f !important;
  background: transparent !important;
}

/* Dropdown arrow icon */
[data-testid="stSidebar"] [data-baseweb="select"] svg {
  fill: #1c0e0f !important;
}

/* Dropdown open — list container */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul {
  background: #ffffff !important;
}

/* Each option item */
[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] li {
  color: #1c0e0f !important;
  background: #ffffff !important;
}

/* Hovered option */
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] li:hover {
  background: #f0e8e8 !important;
  color: #1c0e0f !important;
}

/* Selected/highlighted option */
[data-baseweb="popover"] [aria-selected="true"] {
  background: #e8d5d5 !important;
  color: #1c0e0f !important;
}

[data-testid="stSidebar"] .stMarkdown table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
  border-radius: var(--r-sm);
  overflow: hidden;
}

[data-testid="stSidebar"] .stMarkdown table th {
  background: rgba(244, 208, 63, 0.14) !important;
  color: var(--gold-lt) !important;
  padding: 8px 12px;
  text-align: left;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

[data-testid="stSidebar"] .stMarkdown table td {
  padding: 7px 12px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

[data-testid="stSidebar"] .stMarkdown table tr:last-child td {
  border-bottom: none;
}

[data-testid="stSidebar"] .stCaption p,
[data-testid="stSidebar"] small { color: rgba(255,255,255,0.38) !important; font-size: 0.76rem !important; }

[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }

/* ── Info Banner ───────────────────────────────────────────── */
[data-testid="stInfo"] {
  background: rgba(157,28,32,0.05) !important;
  border-left: 3px solid var(--maroon) !important;
  border-radius: var(--r-sm) !important;
  border-top: none !important;
  border-right: none !important;
  border-bottom: none !important;
}

[data-testid="stInfo"] p { color: var(--text-2) !important; font-size: 0.875rem !important; }

/* ── Placeholder ───────────────────────────────────────────── */
.ce-placeholder {
  border: 2px dashed var(--border);
  border-radius: var(--r-lg);
  padding: 56px 32px;
  text-align: center;
  background: var(--surface);
}

.ce-ph-icon {
  font-size: 3rem;
  margin-bottom: 12px;
  opacity: 0.65;
  display: block;
}

.ce-ph-title {
  font-family: var(--font-display);
  font-size: 1.45rem;
  font-weight: 700;
  margin: 0 0 8px;
}

.ce-ph-body {
  font-size: 0.875rem;
  color: var(--text-3);
  line-height: 1.65;
  margin: 0 auto;
  max-width: 280px;
}

/* ── Result Panels ─────────────────────────────────────────── */
.ce-result-ontime {
  background: linear-gradient(135deg, #0c5c30 0%, #18864a 100%);
  border-radius: var(--r-lg);
  padding: 34px 28px;
  text-align: center;
  color: white;
  box-shadow: 0 8px 36px rgba(12,92,48,0.30);
  margin-bottom: 16px;
  animation: resultBounce 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  position: relative;
  overflow: hidden;
}

.ce-result-delayed {
  background: linear-gradient(135deg, var(--maroon-deep) 0%, var(--maroon) 100%);
  border-radius: var(--r-lg);
  padding: 34px 28px;
  text-align: center;
  color: white;
  box-shadow: 0 8px 36px var(--maroon-glow);
  margin-bottom: 16px;
  animation: resultBounce 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  position: relative;
  overflow: hidden;
}

.ce-result-ontime::after,
.ce-result-delayed::after {
  content: '';
  position: absolute;
  bottom: -30px; right: -30px;
  width: 120px; height: 120px;
  background: radial-gradient(circle, rgba(255,255,255,0.10) 0%, transparent 65%);
  pointer-events: none;
}

@keyframes resultBounce {
  from { opacity: 0; transform: scale(0.88) translateY(10px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}

.ce-res-icon  { font-size: 3rem; margin-bottom: 8px; display: block; }
.ce-res-label {
  font-family: var(--font-display);
  font-size: 1.85rem;
  font-weight: 700;
  color: white;
  margin: 0 0 8px;
  letter-spacing: -0.01em;
}
.ce-res-conf {
  display: inline-block;
  background: rgba(255,255,255,0.15);
  border-radius: 100px;
  padding: 5px 16px;
  font-size: 0.85rem;
  color: rgba(255,255,255,0.90);
  font-weight: 500;
}

/* ── Metric Cards ──────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important;
  padding: 14px 18px !important;
  box-shadow: var(--sh-xs) !important;
}

[data-testid="stMetric"] label {
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  color: var(--text-3) !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
  font-family: var(--font-display) !important;
  font-size: 1.65rem !important;
  font-weight: 700 !important;
  color: var(--maroon) !important;
}

/* ── About Page ────────────────────────────────────────────── */
.ce-about-hero {
  background: linear-gradient(135deg, #1a0e0e 0%, #2d1414 45%, var(--maroon-deep) 100%);
  border-radius: var(--r-xl);
  padding: 56px 48px;
  text-align: center;
  margin-bottom: 36px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--sh-xl);
}

.ce-about-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(244,208,63,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(244,208,63,0.03) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
}

.ce-about-tag {
  display: inline-block;
  background: rgba(244,208,63,0.14);
  border: 1px solid rgba(244,208,63,0.30);
  color: var(--gold-lt);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  padding: 5px 14px;
  border-radius: 100px;
  margin-bottom: 18px;
  position: relative; z-index: 1;
}

.ce-about-title {
  font-family: var(--font-display);
  font-size: 2.6rem;
  font-weight: 700;
  color: #ffffff !important;
  margin: 0 0 10px;
  position: relative; z-index: 1;
}

.ce-about-line {
  width: 56px; height: 3px;
  background: var(--gold);
  border-radius: 2px;
  margin: 16px auto;
  position: relative; z-index: 1;
}

.ce-about-desc {
  color: rgba(255,255,255,0.58);
  font-size: 0.92rem;
  margin: 0;
  position: relative; z-index: 1;
}

.ce-thesis-card {
  background: linear-gradient(135deg, var(--maroon) 0%, var(--maroon-dk) 100%);
  border-radius: var(--r-lg);
  padding: 30px 34px;
  color: white;
  margin-bottom: 28px;
  box-shadow: var(--sh-lg);
  position: relative;
  overflow: hidden;
}

.ce-thesis-card::before {
  content: '\201C';
  position: absolute;
  top: -8px; right: 20px;
  font-family: var(--font-display);
  font-size: 9rem;
  color: rgba(244,208,63,0.10);
  line-height: 1;
  pointer-events: none;
}

.ce-thesis-eye {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--gold-lt);
  opacity: 0.8;
  margin-bottom: 10px;
}

.ce-thesis-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  color: white;
  margin: 0 0 12px;
  line-height: 1.45;
}

.ce-thesis-body {
  font-size: 0.875rem;
  color: rgba(255,255,255,0.72);
  line-height: 1.7;
  margin: 0;
}

.ce-thesis-hl { color: var(--gold-lt); font-weight: 600; }

.ce-section-hd {
  font-family: var(--font-display);
  font-size: 1.7rem;
  font-weight: 700;
  color: var(--maroon);
  margin: 36px 0 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ce-section-hd::after {
  content: '';
  display: block;
  flex: 1;
  height: 1px;
  background: var(--border);
  margin-left: 6px;
}

.ce-person-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 4px solid var(--maroon);
  border-radius: var(--r-lg);
  padding: 28px 20px;
  text-align: center;
  box-shadow: var(--sh-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ce-person-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--sh-lg);
}

.ce-person-card.adviser { border-top-color: var(--gold-dk); }

.ce-avatar {
  width: 78px; height: 78px;
  border-radius: 50%;
  border: 3px solid var(--gold);
  margin: 0 auto 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, var(--maroon), var(--maroon-dk));
}

.ce-avatar.adv {
  background: linear-gradient(135deg, var(--gold-dk), var(--gold));
  color: var(--maroon-deep);
  border-color: var(--gold-dk);
}

.ce-person-name {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 4px;
}

.ce-person-role {
  font-size: 0.70rem;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--maroon);
  margin-bottom: 9px;
  display: block;
}

.ce-person-card.adviser .ce-person-role { color: var(--gold-dk); }

.ce-person-detail {
  font-size: 0.82rem;
  color: var(--text-3);
  line-height: 1.6;
}

.ce-institution {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 28px 32px;
  box-shadow: var(--sh-sm);
}

.ce-inst-name {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 4px;
}

.ce-inst-sub {
  font-size: 0.875rem;
  color: var(--text-3);
  margin: 0 0 18px;
  line-height: 1.5;
}

.ce-inst-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border-lt);
}

.ce-inst-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: var(--maroon-pale);
  color: var(--maroon);
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.ce-footer {
  text-align: center;
  margin-top: 52px;
  padding-top: 24px;
  border-top: 1px solid var(--border-lt);
  font-size: 0.78rem;
  color: var(--text-4);
  line-height: 1.9;
}

/* ── Animations ────────────────────────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.fade-up   { animation: fadeUp 0.48s cubic-bezier(0.22, 1, 0.36, 1) both; }
.delay-1   { animation-delay: 0.08s; }
.delay-2   { animation-delay: 0.16s; }
.delay-3   { animation-delay: 0.24s; }
.delay-4   { animation-delay: 0.32s; }

/* ── Input Styles ──────────────────────────────────────────── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
  border-radius: var(--r-sm) !important;
  border-color: var(--border) !important;
  font-family: var(--font-body) !important;
}

[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
  border-color: var(--maroon) !important;
  box-shadow: 0 0 0 2px var(--maroon-pale) !important;
}

[data-testid="stSlider"] [data-testid="stThumbValue"],
[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
  background: var(--maroon) !important;
  border-color: var(--maroon) !important;
}

[data-testid="stCaptionContainer"] p {
  color: var(--text-3) !important;
  font-size: 0.78rem !important;
}

[data-baseweb="select"] [data-baseweb="select-input"]:focus {
  border-color: var(--maroon) !important;
}

@media (max-width: 640px) {
  .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
}
</style>

<script>
function ceSwitchTab(idx) {
  const tabs = document.querySelectorAll('[data-baseweb="tab"]');
  if (tabs[idx]) { tabs[idx].click(); window.scrollTo({top: 300, behavior: 'smooth'}); }
}
</script>
"""

# ── HTML Templates ─────────────────────────────────────────────

NAVBAR_HTML = f"""
<div class="ce-navbar">
  <div class="ce-nav-logo">
    <div class="ce-nav-logo-mark">{LOGO_IMG_TAG}</div>
    <div class="ce-nav-logo-text">
      <span class="ce-nav-logo-main">CE <em>Predictor</em></span>
      <span class="ce-nav-logo-sub">MSU–Marawi · Civil Engineering</span>
    </div>
  </div>
  <div class="ce-nav-sep"></div>
  <div class="ce-nav-right">
    <div class="ce-nav-pill">
      <span class="ce-nav-pill-dot"></span>
      Thesis Project 2026
    </div>
  </div>
</div>
"""

HERO_HTML = """
<div class="ce-hero">
  <div class="ce-hero-content">
    <div class="ce-hero-badge">
      <span class="ce-badge-dot"></span>
      Thesis Project · Civil Engineering · MSU–Marawi
    </div>
    <h1 class="ce-hero-title">
      CE Graduation
      <span class="ce-hero-accent">Predictor</span>
    </h1>
    <p class="ce-hero-sub">
      Predict on-time graduation of Civil Engineering students
      using machine learning — empowering advisers, supporting students.
    </p>
    <div class="ce-hero-stats">
      <div class="ce-hero-stat">
        <span class="ce-stat-num">3</span>
        <span class="ce-stat-lbl">Models</span>
      </div>
      <div class="ce-hero-stat">
        <span class="ce-stat-num">2</span>
        <span class="ce-stat-lbl">Algorithms</span>
      </div>
      <div class="ce-hero-stat">
        <span class="ce-stat-num">CE</span>
        <span class="ce-stat-lbl">Dept.</span>
      </div>
      <div class="ce-hero-stat">
        <span class="ce-stat-num">ML</span>
        <span class="ce-stat-lbl">Powered</span>
      </div>
    </div>
  </div>
  <div class="ce-hero-visual">
    <svg viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="110" cy="110" r="100" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
      <circle cx="110" cy="110" r="76" stroke="rgba(244,208,63,0.28)" stroke-width="1.5" stroke-dasharray="5 7"/>
      <circle cx="110" cy="110" r="92" stroke="rgba(255,255,255,0.07)" stroke-width="8" fill="none"/>
      <circle cx="110" cy="110" r="92" stroke="#f4d03f" stroke-width="8" fill="none" stroke-dasharray="433 144" stroke-dashoffset="108" stroke-linecap="round"/>
      <circle cx="110" cy="110" r="48" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.10)" stroke-width="1"/>
      <polygon points="110,78 145,94 110,110 75,94" fill="rgba(244,208,63,0.88)" stroke="rgba(244,208,63,0.5)" stroke-width="1"/>
      <path d="M83,101 L83,124 Q110,136 137,124 L137,101" stroke="#f4d03f" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="145" y1="94" x2="145" y2="114" stroke="#f4d03f" stroke-width="2" stroke-linecap="round"/>
      <circle cx="145" cy="117" r="4" fill="#f4d03f"/>
      <circle cx="110" cy="18"  r="5" fill="rgba(244,208,63,0.75)"/>
      <circle cx="202" cy="110" r="4" fill="rgba(244,208,63,0.55)"/>
      <circle cx="18"  cy="110" r="4" fill="rgba(244,208,63,0.55)"/>
      <circle cx="42"  cy="42"  r="3" fill="rgba(255,255,255,0.18)"/>
      <circle cx="178" cy="42"  r="3" fill="rgba(255,255,255,0.18)"/>
      <circle cx="42"  cy="178" r="3" fill="rgba(255,255,255,0.18)"/>
      <circle cx="178" cy="178" r="3" fill="rgba(255,255,255,0.18)"/>
      <line x1="110" y1="23"  x2="110" y2="60"  stroke="rgba(244,208,63,0.18)" stroke-width="1"/>
      <line x1="197" y1="110" x2="160" y2="110" stroke="rgba(244,208,63,0.18)" stroke-width="1"/>
      <line x1="23"  y1="110" x2="60"  y2="110" stroke="rgba(244,208,63,0.18)" stroke-width="1"/>
    </svg>
  </div>
</div>
"""

MODELS_OVERVIEW_HTML = """
<div class="ce-models-row fade-up">
  <div class="ce-model-card" onclick="ceSwitchTab(0)">
    <div class="ce-model-num">01</div>
    <div class="ce-model-name">Pre-Admission</div>
    <div class="ce-model-desc">SASE scores and SHS background — before university subjects are taken.</div>
    <span class="ce-model-tag">Best at admission</span>
  </div>
  <div class="ce-model-card" onclick="ceSwitchTab(1)">
    <div class="ce-model-num">02</div>
    <div class="ce-model-name">In-Program</div>
    <div class="ce-model-desc">Critical grades, CGPA, and retake history — during the program.</div>
    <span class="ce-model-tag">Each semester</span>
  </div>
  <div class="ce-model-card" onclick="ceSwitchTab(2)">
    <div class="ce-model-num">03</div>
    <div class="ce-model-name">Combined</div>
    <div class="ce-model-desc">Full profile combining all pre-admission and in-program features.</div>
    <span class="ce-model-tag">Complete analysis</span>
  </div>
</div>
"""

RESULT_HTML = """
<div class="{css_class}">
  <span class="ce-res-icon">{icon}</span>
  <p class="ce-res-label">{label}</p>
  <span class="ce-res-conf">Confidence: <strong>{confidence:.1f}%</strong></span>
</div>
"""

PLACEHOLDER_HTML = """
<div class="ce-placeholder fade-up">
  <span class="ce-ph-icon">{icon}</span>
  <h3 class="ce-ph-title" style="color:{color}">{title}</h3>
  <p class="ce-ph-body">{body}</p>
</div>
"""
