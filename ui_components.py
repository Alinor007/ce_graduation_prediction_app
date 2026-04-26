"""
ui_components.py
Reusable Streamlit UI components — MSU-CE branded redesign.
Color palette pulled from the Civil Engineering Department logo:
  Crimson  #C8102E   Gold    #F5A800   White   #FFFFFF   Black   #1A1A1A
"""

import numpy as np
import streamlit as st

import charts
from config import (
    ALL_STRANDS,
    GRADE_COLS_LEFT,
    GRADE_COLS_RIGHT,
    GWA_OPTIONS,
)
from predictor import AlgorithmResult, PredictionResult, get_feature_importances


# ── Valid Philippine Grading Scale values ─────────────────────
PH_GRADE_OPTIONS = [None, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 2.75, 3.0, 5.0]
PH_GRADE_LABELS  = {
    None: "— Not taken —",
    1.0:  "1.0  ·  Excellent",
    1.25: "1.25 ·  Between Excellent – Very Good",
    1.5:  "1.5  ·  Very Good",
    1.75: "1.75 ·  Between Very Good – Good",
    2.0:  "2.0  ·  Good",
    2.5:  "2.5  ·  Satisfactory",
    2.75: "2.75 ·  Between Satisfactory – Passing",
    3.0:  "3.0  ·  Lowest Passing",
    5.0:  "5.0  ·  Failed",
}

# ── CSS ───────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600;700&display=swap');

/* ── Root variables ── */
:root {
  --crimson:     #C8102E;
  --crimson-dk:  #960020;
  --gold:        #F5A800;
  --gold-lt:     #FFD166;
  --white:       #FFFFFF;
  --off-white:   #FAF8F5;
  --black:       #1A1A1A;
  --gray:        #6B7280;
  --light-gray:  #F0F0F0;
  --border:      #E2E2E2;
  --shadow:      0 4px 24px rgba(200,16,46,0.10);
  --shadow-lg:   0 8px 40px rgba(200,16,46,0.18);
}

html, body, [class*="css"] {
  font-family: 'Source Sans 3', sans-serif;
  background: var(--off-white);
  color: var(--black);
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Animated page background ── */
.stApp {
  background:
    radial-gradient(ellipse 80% 50% at 10% -10%, rgba(200,16,46,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 110%, rgba(245,168,0,0.07) 0%, transparent 60%),
    var(--off-white);
  min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(160deg, #1A1A1A 0%, #2D0008 60%, #1A1A1A 100%) !important;
  border-right: 3px solid var(--gold);
}
[data-testid="stSidebar"] * { color: #F5F5F5 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--gold) !important; }
/* Fix selectbox text inside sidebar */
[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="input-container"],
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="valueContainer"] {
  color: #1A1A1A !important;
}
[data-testid="stSidebar"] .stMarkdown table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}
[data-testid="stSidebar"] .stMarkdown table th {
  background: rgba(245,168,0,0.25);
  color: var(--gold-lt) !important;
  padding: 6px 10px;
  text-align: left;
}
[data-testid="stSidebar"] .stMarkdown table td {
  padding: 5px 10px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] .stMarkdown table tr:last-child td {
  border-bottom: none;
}

/* ── Hero banner ── */
.hero {
  background: linear-gradient(130deg, var(--crimson-dk) 0%, var(--crimson) 45%, #8B0000 100%);
  border-radius: 20px;
  padding: 36px 44px 32px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  animation: heroReveal 0.7s cubic-bezier(.22,1,.36,1) both;
}
@keyframes heroReveal {
  from { opacity: 0; transform: translateY(-18px); }
  to   { opacity: 1; transform: translateY(0); }
}
.hero::before {
  content: '';
  position: absolute; top: -60px; right: -60px;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(245,168,0,0.18) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 4s ease-in-out infinite;
}
.hero::after {
  content: '';
  position: absolute; bottom: -40px; left: 20%;
  width: 160px; height: 160px;
  background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
  border-radius: 50%;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50%       { transform: scale(1.12); opacity: 1; }
}
.hero-badge {
  display: inline-block;
  background: var(--gold);
  color: var(--black);
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  padding: 4px 14px; border-radius: 20px;
  margin-bottom: 14px;
  animation: heroReveal 0.7s 0.1s both;
}
.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: 2.1rem; font-weight: 900;
  color: #fff; margin: 0 0 6px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.3);
  animation: heroReveal 0.7s 0.15s both;
}
.hero p {
  color: rgba(255,255,255,0.78);
  font-size: 0.95rem; margin: 0;
  animation: heroReveal 0.7s 0.2s both;
}
.hero-logo {
  position: absolute; right: 32px; top: 50%;
  transform: translateY(-50%);
  width: 90px; height: 90px;
  opacity: 0.15;
  filter: brightness(10);
}

/* ── Section cards ── */
.section-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-top: 3px solid var(--crimson);
  border-radius: 14px;
  padding: 22px 26px;
  margin-bottom: 18px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: box-shadow 0.25s;
  animation: cardIn 0.5s cubic-bezier(.22,1,.36,1) both;
}
.section-card:hover {
  box-shadow: 0 6px 28px rgba(200,16,46,0.12);
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.section-title {
  font-size: 0.72rem; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: var(--crimson);
  border-bottom: 2px solid var(--gold);
  padding-bottom: 6px; margin-bottom: 16px;
  display: inline-block;
}

/* ── Grade note ── */
.grade-note {
  background: #FFF8E1;
  border-left: 4px solid var(--gold);
  border-radius: 0 10px 10px 0;
  padding: 10px 15px;
  font-size: 0.83rem; color: #6D4C00;
  margin-bottom: 14px;
}

/* ── SASE total box ── */
.sase-total-box {
  background: linear-gradient(135deg, var(--crimson) 0%, var(--crimson-dk) 100%);
  border-radius: 12px; padding: 14px 20px;
  margin-bottom: 14px; text-align: center;
  box-shadow: 0 4px 16px rgba(200,16,46,0.25);
}
.sase-total-box .label { font-size: .72rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gold-lt); }
.sase-total-box .value { font-size: 2.2rem; font-weight: 700; color: #fff; line-height: 1.1; }
.sase-total-box .hint  { font-size: .73rem; color: rgba(255,255,255,0.65); margin-top: 3px; }

/* ── Result panels ── */
.result-ontime {
  background: linear-gradient(135deg, #155C30 0%, #1E8449 100%);
  border-radius: 16px; padding: 30px 34px; text-align: center;
  color: white; box-shadow: 0 8px 32px rgba(30,132,73,.28);
  animation: resultBounce 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
.result-delayed {
  background: linear-gradient(135deg, var(--crimson-dk) 0%, var(--crimson) 100%);
  border-radius: 16px; padding: 30px 34px; text-align: center;
  color: white; box-shadow: 0 8px 32px rgba(200,16,46,.28);
  animation: resultBounce 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes resultBounce {
  from { opacity: 0; transform: scale(0.88); }
  to   { opacity: 1; transform: scale(1); }
}
.result-icon  { font-size: 3.2rem; margin-bottom: 6px; }
.result-label { font-family: 'Playfair Display', serif; font-size: 1.65rem; font-weight: 700; margin: 0; }
.result-sub   { font-size: .88rem; opacity: .82; margin-top: 5px; }

/* ── Predict button ── */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, var(--crimson) 0%, var(--crimson-dk) 100%);
  color: white; font-weight: 700; font-size: 1rem;
  border: none; border-radius: 12px;
  padding: 14px 28px; width: 100%; cursor: pointer;
  box-shadow: 0 4px 18px rgba(200,16,46,0.3);
  transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s;
  letter-spacing: 0.5px;
}
div[data-testid="stButton"] > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(200,16,46,0.4);
}
div[data-testid="stButton"] > button:active {
  transform: translateY(0);
}

/* ── Tab bar ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent;
  gap: 6px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  border-radius: 10px 10px 0 0 !important;
  font-weight: 600;
  border: 1px solid var(--border) !important;
  border-bottom: none !important;
  background: var(--white) !important;
  color: var(--gray) !important;
  transition: background 0.2s, color 0.2s;
}
[data-testid="stTabs"] [aria-selected="true"] {
  background: var(--crimson) !important;
  color: var(--white) !important;
  border-color: var(--crimson) !important;
}

/* ── Placeholder ── */
.placeholder-box {
  border-radius: 16px; padding: 44px 32px;
  text-align: center; margin-top: 6px;
  border: 2px dashed var(--border);
  background: var(--white);
}

/* ── About page ── */
.about-hero {
  background: linear-gradient(130deg, #1A1A1A 0%, #2D0008 50%, #1A1A1A 100%);
  border-radius: 20px; padding: 40px 48px;
  text-align: center; margin-bottom: 32px;
  position: relative; overflow: hidden;
  box-shadow: var(--shadow-lg);
}
.about-hero::before {
  content: ''; position: absolute; inset: 0;
  background: repeating-linear-gradient(
    45deg, transparent, transparent 40px,
    rgba(245,168,0,0.03) 40px, rgba(245,168,0,0.03) 80px
  );
}
.about-hero h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.9rem; color: #fff; margin: 0 0 8px;
}
.about-hero p { color: rgba(255,255,255,0.65); font-size: 0.92rem; margin: 0; }
.about-hero .gold-line {
  width: 60px; height: 3px;
  background: var(--gold);
  border-radius: 2px;
  margin: 16px auto;
}

.person-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-top: 4px solid var(--crimson);
  border-radius: 16px;
  padding: 28px 22px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  transition: transform 0.25s, box-shadow 0.25s;
  animation: cardIn 0.5s cubic-bezier(.22,1,.36,1) both;
}
.person-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 36px rgba(200,16,46,0.16);
}
.person-avatar {
  width: 100px; height: 100px;
  border-radius: 50%;
  border: 3px solid var(--gold);
  margin: 0 auto 14px;
  object-fit: cover;
  display: block;
  background: var(--light-gray);
}
.person-avatar-placeholder {
  width: 100px; height: 100px;
  border-radius: 50%;
  border: 3px solid var(--gold);
  margin: 0 auto 14px;
  background: linear-gradient(135deg, var(--crimson) 0%, var(--crimson-dk) 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 2.2rem; color: white;
}
.person-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem; font-weight: 700;
  color: var(--black); margin: 0 0 4px;
}
.person-role {
  font-size: 0.78rem; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--crimson); margin-bottom: 8px;
}
.person-detail {
  font-size: 0.82rem; color: var(--gray);
  line-height: 1.55;
}

.adviser-card {
  border-top: 4px solid var(--gold) !important;
}
.adviser-card .person-role { color: #8B6800; }
.adviser-avatar-placeholder {
  background: linear-gradient(135deg, var(--gold) 0%, #D4890A 100%);
}

.thesis-info-card {
  background: linear-gradient(135deg, var(--crimson) 0%, var(--crimson-dk) 100%);
  border-radius: 16px; padding: 28px 32px;
  color: white; margin-bottom: 24px;
  box-shadow: var(--shadow);
}
.thesis-info-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem; margin: 0 0 6px;
  color: var(--gold-lt);
}
.thesis-info-card p { margin: 0; opacity: 0.85; font-size: 0.88rem; line-height: 1.6; }

.suggest-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-left: 4px solid var(--gold);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 12px;
  transition: transform 0.2s;
}
.suggest-card:hover { transform: translateX(4px); }
.suggest-card h4 { margin: 0 0 4px; color: var(--black); font-size: 0.95rem; }
.suggest-card p  { margin: 0; color: var(--gray); font-size: 0.83rem; line-height: 1.5; }

/* ── Scroll reveal animation helper ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp 0.55s cubic-bezier(.22,1,.36,1) both; }
.delay-1 { animation-delay: 0.08s; }
.delay-2 { animation-delay: 0.16s; }
.delay-3 { animation-delay: 0.24s; }
.delay-4 { animation-delay: 0.32s; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 18px !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
</style>
"""


# ── Static HTML templates ─────────────────────────────────────

_HERO_HTML = """
<div class="hero">
  <div class="hero-badge">Thesis Project · Civil Engineering · MSU–Marawi</div>
  <h1>🎓 CE Graduation Predictor</h1>
  <p>Predicting On-Time Graduation of Civil Engineering Students using Machine Learning</p>
</div>
"""

_RESULT_HTML = """
<div class="{css_class}">
  <div class="result-icon">{icon}</div>
  <p class="result-label">{label}</p>
  <p class="result-sub">Confidence: <strong>{confidence:.1f}%</strong></p>
</div>
"""

_PLACEHOLDER_HTML = """
<div class="placeholder-box fade-up">
  <div style="font-size:3rem;margin-bottom:8px">{icon}</div>
  <h3 style="color:{color};font-family:'Playfair Display',serif;margin:0 0 8px">{title}</h3>
  <p style="color:#6B7280;font-size:.9rem;margin:0">{body}</p>
</div>
"""


# ── Top-level page components ─────────────────────────────────

def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(_HERO_HTML, unsafe_allow_html=True)


def render_sidebar(algorithms: list[str]) -> str:
    """Render sidebar controls and return the chosen algorithm name."""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        chosen = st.selectbox("Algorithm", algorithms)
        st.markdown("---")
        st.markdown("""
**📘 Philippine Grading Scale**

| Grade | Meaning |
|---|---|
| 1.0 | Excellent |
| 1.25 | Between Excellent–Very Good |
| 1.5 | Very Good |
| 1.75 | Between Very Good–Good |
| 2.0 | Good |
| 2.5 | Satisfactory |
| 2.75 | Between Satisfactory–Passing |
| 3.0 | Lowest Passing |
| 5.0 | Failed |
""")
        st.markdown("---")
        st.markdown("""
**📐 Model Framework**

| Model | Use When |
|---|---|
| **Model 1** | At admission |
| **Model 2** | Each semester |
| **Model 3** | Full profile available |
""")
        st.markdown("---")
        st.caption("Decision-support tool only. Always combine with human judgment.")
    return chosen


# ── Input section components ──────────────────────────────────

def card_open(title: str) -> None:
    st.markdown(
        f'<div class="section-card"><span class="section-title">{title}</span>',
        unsafe_allow_html=True,
    )


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def grade_note(text: str) -> None:
    st.markdown(f'<div class="grade-note">{text}</div>', unsafe_allow_html=True)


def sase_inputs(prefix: str) -> tuple[float, float, float, float, float]:
    grade_note("From the student's admission records. Total SASE is automatically computed.")
    col_left, col_right = st.columns(2)
    with col_left:
        math = st.number_input("Mathematics",         min_value=0.0, max_value=80.0,  value=20.0, step=1.0, key=f"{prefix}_ma")
        sci  = st.number_input("Science",             min_value=0.0, max_value=60.0,  value=10.0, step=1.0, key=f"{prefix}_sci")
    with col_right:
        lang = st.number_input("Language Arts",       min_value=0.0, max_value=80.0,  value=35.0, step=1.0, key=f"{prefix}_la")
        abst = st.number_input("Abstract/Perceptual", min_value=0.0, max_value=60.0,  value=15.0, step=1.0, key=f"{prefix}_ap")

    total = math + lang + sci + abst
    st.markdown(
        f"""<div class="sase-total-box">
            <div class="label">Total SASE (Auto-Computed)</div>
            <div class="value">{total:.0f}</div>
            <div class="hint">Math ({math:.0f}) + Language Arts ({lang:.0f}) + Science ({sci:.0f}) + Abstract ({abst:.0f})</div>
        </div>""",
        unsafe_allow_html=True,
    )
    return total, math, lang, sci, abst


def shs_inputs(prefix: str) -> tuple[float, str]:
    gwa_band = st.selectbox(
        "SHS GWA Band", list(GWA_OPTIONS.keys()), index=2, key=f"{prefix}_gwa",
        help="Select the student's Senior High School GWA range",
    )
    gwa_num = GWA_OPTIONS[gwa_band]
    st.caption(f"Encoded as numeric midpoint: **{gwa_num}**")
    strand = st.selectbox("SHS Strand", ALL_STRANDS, key=f"{prefix}_strand")
    return gwa_num, strand


def grade_inputs(prefix: str) -> dict[str, float]:
    grade_note(
        "📝 Select the grade for each subject taken using the Philippine Grading Scale. "
        "<strong>Leave it as '— Not taken —' if the subject has not been taken yet</strong> — "
        "the model handles missing values automatically."
    )
    grades: dict[str, float] = {}
    col_left, col_right = st.columns(2)

    def _subject_input(col, subject: str) -> float:
        selected = col.selectbox(
            label=subject,
            options=PH_GRADE_OPTIONS,
            index=0,
            format_func=lambda v: PH_GRADE_LABELS[v],
            key=f"{prefix}_{subject}",
        )
        return float(selected) if selected is not None else np.nan

    with col_left:
        for subject in GRADE_COLS_LEFT:
            grades[subject] = _subject_input(col_left, subject)

    with col_right:
        for subject in GRADE_COLS_RIGHT:
            grades[subject] = _subject_input(col_right, subject)

    taken_count = sum(1 for v in grades.values() if not np.isnan(v))
    st.caption(f"✅ {taken_count} / {len(grades)} subjects filled in")
    return grades


def academic_standing_inputs(prefix: str, grades: dict[str, float]) -> tuple[float, float, float, float, float]:
    cgpa = st.slider("CGPA", min_value=1.0, max_value=3.0, value=2.40, step=0.01, format="%.2f", key=f"{prefix}_cgpa")

    valid_grades = [v for v in grades.values() if not (isinstance(v, float) and np.isnan(v))]
    _valid_ph = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 2.75, 3.0, 5.0]
    if valid_grades:
        raw_avg = float(np.mean(valid_grades))
        suggested_avg = min(_valid_ph, key=lambda g: abs(g - raw_avg))
    else:
        suggested_avg = 2.5
    suggested_hard = int(sum(1 for v in valid_grades if v >= 3.0))

    col_left, col_right = st.columns(2)
    with col_left:
        total_retakes = st.number_input(
            "Total Retakes", min_value=0, max_value=30, value=2, step=1,
            key=f"{prefix}_tr", help="Total extra subject attempts across all subjects",
        )
        avg_grade = st.selectbox(
            "Average Grade",
            options=_valid_ph,
            index=_valid_ph.index(suggested_avg),
            format_func=lambda v: PH_GRADE_LABELS[v],
            key=f"{prefix}_avg",
            help="Auto-suggested from grades above (snapped to valid PH grade); adjust if needed",
        )
    with col_right:
        max_retake = st.number_input(
            "Max Single Retake", min_value=0, max_value=10, value=1, step=1,
            key=f"{prefix}_mr", help="Worst single subject: how many extra attempts?",
        )
        hard_fails = st.number_input(
            "Hard Fails (3.00)", min_value=0, max_value=20,
            value=suggested_hard, step=1,
            key=f"{prefix}_hf", help="Auto-suggested from grades above; adjust if needed",
        )

    return cgpa, float(total_retakes), float(max_retake), float(avg_grade), float(hard_fails)


# ── Result panel components ───────────────────────────────────

def _render_result_banner(result: PredictionResult) -> None:
    if result.is_ontime:
        html = _RESULT_HTML.format(
            css_class="result-ontime", icon="✅",
            label="ON-TIME GRADUATION", confidence=result.prob_ontime * 100,
        )
    else:
        html = _RESULT_HTML.format(
            css_class="result-delayed", icon="⚠️",
            label="DELAYED GRADUATION", confidence=result.prob_delayed * 100,
        )
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def _render_probability_section(result: PredictionResult) -> None:
    card_open("📈 Probability Breakdown")
    col_left, col_right = st.columns(2)
    col_left.metric("✅ On-Time", f"{result.prob_ontime * 100:.1f}%")
    col_right.metric("⚠️ Delayed", f"{result.prob_delayed * 100:.1f}%")
    fig = charts.gauge(result.prob_ontime)
    st.pyplot(fig, use_container_width=True)
    plt_close()
    card_close()


def _render_risk_section(result: PredictionResult) -> None:
    risk_messages = {
        "low":      "🟢 **Low Risk** — Strong on-time indicators. Continue monitoring each semester.",
        "moderate": "🟡 **Moderate Risk** — Borderline. Recommend proactive academic advising.",
        "high":     "🔴 **High Risk** — Immediate academic intervention recommended.",
    }
    card_open("💡 Risk Interpretation")
    st.markdown(risk_messages[result.risk_level])
    card_close()


def _render_comparison_section(algo_results: list[AlgorithmResult]) -> None:
    card_open("🤖 Algorithm Comparison")
    fig = charts.algorithm_comparison(algo_results)
    st.pyplot(fig, use_container_width=True)
    plt_close()
    card_close()


def _render_importance_section(model_bundle: dict, features: list[str]) -> None:
    card_open("📊 Feature Importance (Random Forest)")
    importance_pairs = get_feature_importances(model_bundle, features)
    fig = charts.feature_importance(importance_pairs)
    st.pyplot(fig, use_container_width=True)
    plt_close()
    card_close()


def render_results(
    result: PredictionResult,
    algo_results: list[AlgorithmResult],
    model_bundle: dict,
    features: list[str],
) -> None:
    _render_result_banner(result)
    _render_probability_section(result)
    _render_risk_section(result)
    _render_comparison_section(algo_results)
    _render_importance_section(model_bundle, features)


def render_placeholder(bg: str, icon: str, color: str, title: str, body: str) -> None:
    st.markdown(
        _PLACEHOLDER_HTML.format(bg=bg, icon=icon, color=color, title=title, body=body),
        unsafe_allow_html=True,
    )


# ── About page ────────────────────────────────────────────────

def render_about_page() -> None:
    st.markdown("""
<div class="about-hero fade-up">
  <h2>About This Project</h2>
  <div class="gold-line"></div>
  <p>Mindanao State University – Main Campus, Marawi City · Civil Engineering Department · January 2026</p>
</div>
""", unsafe_allow_html=True)

    # Thesis title card
    st.markdown("""
<div class="thesis-info-card fade-up delay-1">
  <h3>📖 Thesis Title</h3>
  <p style="font-size:0.95rem;font-weight:600;margin-bottom:8px">
    A Predictive Analytics Study on the Key Determinants of On-Time Completion of Civil Engineering Students at MSU–Marawi
  </p>
  <p>
    An Undergraduate Thesis presented to the Faculty of the Civil Engineering Department,
    College of Engineering, in partial fulfillment of the requirements for the Degree of
    <strong style="color:#FFD166">Bachelor of Science in Civil Engineering</strong>.
  </p>
</div>
""", unsafe_allow_html=True)

    # Authors
    st.markdown('<h3 style="font-family:\'Playfair Display\',serif;color:#C8102E;margin:28px 0 18px;font-size:1.4rem">👥 Authors</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    authors = [
        ("Bilao, Jonaif H.",         "BS Civil Engineering", "Research Lead"),
        ("Dibaratun, Norhan L.",      "BS Civil Engineering", "Data Analysis"),
        ("Villamor, Airene Grace L.", "BS Civil Engineering", "Model Development"),
    ]
    initials = ["JB", "ND", "AV"]

    for col, (name, degree, role), init in zip([col1, col2, col3], authors, initials):
        with col:
            st.markdown(f"""
<div class="person-card fade-up delay-2">
  <div class="person-avatar-placeholder" style="display:flex;align-items:center;justify-content:center;font-size:2rem;color:white;font-weight:700;width:100px;height:100px;border-radius:50%;border:3px solid #F5A800;margin:0 auto 14px;background:linear-gradient(135deg,#C8102E,#960020)">
    {init}
  </div>
  <div class="person-name">{name}</div>
  <div class="person-role">Author</div>
  <div class="person-detail">{degree}<br><em>{role}</em></div>
</div>
""", unsafe_allow_html=True)

    # Adviser
    st.markdown('<h3 style="font-family:\'Playfair Display\',serif;color:#8B6800;margin:32px 0 18px;font-size:1.4rem">🎓 Thesis Adviser</h3>', unsafe_allow_html=True)

    _, adv_col, _ = st.columns([1, 2, 1])
    with adv_col:
        st.markdown("""
<div class="person-card adviser-card fade-up delay-3" style="border-top:4px solid #F5A800">
  <div style="display:flex;align-items:center;justify-content:center;font-size:2.2rem;color:white;font-weight:700;width:100px;height:100px;border-radius:50%;border:3px solid #F5A800;margin:0 auto 14px;background:linear-gradient(135deg,#F5A800,#D4890A)">
    ND
  </div>
  <div class="person-name">Engr. Nhour R. Dibangkitun</div>
  <div class="person-role" style="color:#8B6800">Thesis Adviser</div>
  <div class="person-detail">
    Civil Engineering Department<br>
    College of Engineering<br>
    Mindanao State University – Main Campus
  </div>
</div>
""", unsafe_allow_html=True)

    # Institution
    st.markdown('<h3 style="font-family:\'Playfair Display\',serif;color:#C8102E;margin:32px 0 18px;font-size:1.4rem">🏛️ Institution</h3>', unsafe_allow_html=True)
    st.markdown("""
<div class="section-card fade-up delay-4">
  <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap">
    <div>
      <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#1A1A1A">Mindanao State University – Main Campus</div>
      <div style="font-size:0.88rem;color:#6B7280;margin-top:4px">Civil Engineering Department · College of Engineering</div>
      <div style="font-size:0.85rem;color:#6B7280">Marawi City, Lanao del Sur, Philippines</div>
    </div>
  </div>
  <div style="margin-top:14px;padding-top:14px;border-top:1px solid #E2E2E2;font-size:0.85rem;color:#6B7280">
    <strong style="color:#C8102E">Program:</strong> Bachelor of Science in Civil Engineering (2018 Curriculum) &nbsp;|&nbsp;
    <strong style="color:#C8102E">Year:</strong> January 2026
  </div>
</div>
""", unsafe_allow_html=True)

    # UI Suggestions
    st.markdown('<h3 style="font-family:\'Playfair Display\',serif;color:#C8102E;margin:32px 0 18px;font-size:1.4rem">💡 Suggested Future Enhancements</h3>', unsafe_allow_html=True)

    suggestions = [
        ("📊 Batch Prediction via CSV Upload",
         "Allow advisers to upload a class roster (CSV) and receive predictions for all students in one run, downloadable as a report."),
        ("📅 Semester Progress Tracker",
         "A timeline view showing a student's predicted risk level each semester, tracking how it evolves over their academic journey."),
        ("🔔 At-Risk Student Alert Dashboard",
         "A department-level dashboard listing all flagged high-risk students with recommended interventions and assigned counselors."),
        ("📝 Printable Student Report Card",
         "Generate a PDF summary of a student's prediction results, probability scores, and feature importances for advising sessions."),
        ("🔍 What-If Simulator",
         "Let advisers simulate 'what if the student retakes MAT060?' and see how the prediction score changes in real time."),
        ("📈 Historical Cohort Analytics",
         "Visualize graduation trends by strand, SASE band, and year — helping the department understand systemic patterns over time."),
    ]

    for i, (title, desc) in enumerate(suggestions):
        st.markdown(f"""
<div class="suggest-card fade-up" style="animation-delay:{0.05*i}s">
  <h4>{title}</h4>
  <p>{desc}</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="text-align:center;margin-top:40px;padding-top:24px;border-top:1px solid #E2E2E2;font-size:0.8rem;color:#9CA3AF">
  CE Graduation Predictor · Mindanao State University – Marawi · 2026<br>
  <em>Decision-support tool only. Always combine with human judgment.</em>
</div>
""", unsafe_allow_html=True)


# ── Utility ───────────────────────────────────────────────────

def plt_close() -> None:
    import matplotlib.pyplot as plt
    plt.close()
