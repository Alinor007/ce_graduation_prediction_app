# ============================================================
#  🎓 CE Graduation Predictor — Streamlit App (v2)
#  Two-System Prediction:
#    System A → Incoming Freshmen (SASE scores only)
#    System B → All Year Levels (Full academic profile)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="CE Graduation Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background: #f5f7fa; }
    [data-testid="stSidebar"] { background: #1a3a5c !important; }
    [data-testid="stSidebar"] * { color: #ecf0f1 !important; }
    .hero {
        background: linear-gradient(135deg, #1a3a5c 0%, #0d2137 60%, #1a3a5c 100%);
        border-radius: 16px; padding: 32px 40px; margin-bottom: 24px; position: relative; overflow: hidden;
    }
    .hero::before {
        content:''; position:absolute; top:-40px; right:-40px;
        width:220px; height:220px; background:rgba(232,184,75,0.12); border-radius:50%;
    }
    .hero h1 { font-family:'DM Serif Display',serif; font-size:2rem; color:#fff; margin:0 0 8px 0; }
    .hero p  { color:#a8c0d6; font-size:0.95rem; margin:0; }
    .badge   { display:inline-block; background:#e8b84b; color:#1a1a1a; font-size:0.72rem;
               font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
               padding:4px 12px; border-radius:20px; margin-bottom:12px; }
    .section-card {
        background:#fff; border:1px solid #dce3ed; border-radius:12px;
        padding:22px 26px; margin-bottom:18px; box-shadow:0 2px 8px rgba(0,0,0,.05);
    }
    .section-title {
        font-size:.75rem; font-weight:700; letter-spacing:1.8px; text-transform:uppercase;
        color:#1a3a5c; border-bottom:2px solid #e8b84b; padding-bottom:6px;
        margin-bottom:16px; display:inline-block;
    }
    .result-ontime {
        background:linear-gradient(135deg,#1e8449,#27ae60); border-radius:14px;
        padding:28px 32px; text-align:center; color:white;
        box-shadow:0 8px 24px rgba(30,132,73,.25);
    }
    .result-delayed {
        background:linear-gradient(135deg,#c0392b,#e74c3c); border-radius:14px;
        padding:28px 32px; text-align:center; color:white;
        box-shadow:0 8px 24px rgba(192,57,43,.25);
    }
    .result-icon  { font-size:3rem; margin-bottom:4px; }
    .result-label { font-size:1.7rem; font-weight:700; margin:0; }
    .result-sub   { font-size:.9rem; opacity:.85; margin-top:4px; }
    .grade-note {
        background:#fef9e7; border-left:4px solid #e8b84b;
        border-radius:0 8px 8px 0; padding:9px 14px;
        font-size:.83rem; color:#7d6608; margin-bottom:14px;
    }
    .sase-total-box {
        background:#eaf2fb; border:2px solid #1a3a5c; border-radius:10px;
        padding:12px 18px; margin-bottom:14px; text-align:center;
    }
    .sase-total-box .label { font-size:.75rem; font-weight:700; letter-spacing:1.5px;
        text-transform:uppercase; color:#1a3a5c; }
    .sase-total-box .value { font-size:2rem; font-weight:700; color:#1a3a5c; }
    .sase-total-box .hint  { font-size:.75rem; color:#5d6d7e; margin-top:2px; }
    div[data-testid="stButton"] > button {
        background:linear-gradient(135deg,#1a3a5c,#0d2137); color:white;
        font-weight:700; font-size:1rem; border:none; border-radius:10px;
        padding:13px 28px; width:100%; cursor:pointer;
    }
    div[data-testid="stButton"] > button:hover { opacity:.85; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FEATURE LISTS — must match your notebook exactly
# ─────────────────────────────────────────────────────────────
FEATURES_A = ['SASE_GS', 'SASE_MA', 'SASE_LA', 'SASE_SCI', 'SASE_AP']

FEATURES_B = [
    'SASE_GS', 'SASE_MA', 'SASE_LA', 'SASE_SCI', 'SASE_AP',
    'MAT060', 'MAT070', 'ENS161',
    'CVE151', 'CVE155', 'CVE161', 'CVE195', 'CVE196', 'CVE111', 'CVE112',
    'CGPA',
    'TOTAL_RETAKES', 'MAX_RETAKE', 'AVG_GRADE', 'HARD_FAILS',
]

FEATURE_LABELS = {
    'SASE_GS':'SASE Total','SASE_MA':'SASE Math','SASE_LA':'SASE Language Arts',
    'SASE_SCI':'SASE Science','SASE_AP':'SASE Abstract/Perceptual',
    'MAT060':'MAT060','MAT070':'MAT070','ENS161':'ENS161',
    'CVE151':'CVE151','CVE155':'CVE155','CVE161':'CVE161',
    'CVE195':'CVE195','CVE196':'CVE196','CVE111':'CVE111','CVE112':'CVE112',
    'CGPA':'CGPA','TOTAL_RETAKES':'Total Retakes','MAX_RETAKE':'Max Retake',
    'AVG_GRADE':'Avg Grade','HARD_FAILS':'Hard Fails (3.00)',
}

MODEL_ORDER = ['Random Forest', 'Logistic Regression', 'Decision Tree']

# ─────────────────────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')

@st.cache_resource
def load_models():
    required = [
        'model_A_rf.pkl','model_A_lr.pkl','model_A_dt.pkl','imputer_A.pkl','scaler_A.pkl',
        'model_B_rf.pkl','model_B_lr.pkl','model_B_dt.pkl','imputer_B.pkl','scaler_B.pkl',
    ]
    missing = [f for f in required if not os.path.exists(os.path.join(MODEL_DIR, f))]
    if missing:
        return None, missing
    def p(f): return os.path.join(MODEL_DIR, f)
    return {
        'A': {
            'Random Forest':       joblib.load(p('model_A_rf.pkl')),
            'Logistic Regression': joblib.load(p('model_A_lr.pkl')),
            'Decision Tree':       joblib.load(p('model_A_dt.pkl')),
            'imputer':             joblib.load(p('imputer_A.pkl')),
            'scaler':              joblib.load(p('scaler_A.pkl')),
        },
        'B': {
            'Random Forest':       joblib.load(p('model_B_rf.pkl')),
            'Logistic Regression': joblib.load(p('model_B_lr.pkl')),
            'Decision Tree':       joblib.load(p('model_B_dt.pkl')),
            'imputer':             joblib.load(p('imputer_B.pkl')),
            'scaler':              joblib.load(p('scaler_B.pkl')),
        },
    }, []

# ─────────────────────────────────────────────────────────────
# PREDICTION HELPERS
# ─────────────────────────────────────────────────────────────
def run_prediction(sys_dict, inputs, features, model_name):
    df_in     = pd.DataFrame([inputs])[features]
    df_imp    = sys_dict['imputer'].transform(df_in)
    df_scaled = sys_dict['scaler'].transform(df_imp)
    label     = int(sys_dict[model_name].predict(df_scaled)[0])
    probs     = sys_dict[model_name].predict_proba(df_scaled)[0]
    return label, probs

def run_all_models(sys_dict, inputs, features):
    df_in     = pd.DataFrame([inputs])[features]
    df_imp    = sys_dict['imputer'].transform(df_in)
    df_scaled = sys_dict['scaler'].transform(df_imp)
    return [(n, int(sys_dict[n].predict(df_scaled)[0]), sys_dict[n].predict_proba(df_scaled)[0])
            for n in MODEL_ORDER]

# ─────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────
def plot_gauge(p):
    fig, ax = plt.subplots(figsize=(5,.65)); fig.patch.set_alpha(0); ax.set_facecolor("none")
    ax.barh(0, 1, color="#dce3ed", height=.5)
    ax.barh(0, p, color="#1e8449" if p>=.5 else "#c0392b", height=.5)
    ax.axvline(.5,color="#1a3a5c",linewidth=1.5,linestyle="--",alpha=.6)
    ax.set_xlim(0,1); ax.set_ylim(-.5,.5); ax.axis("off")
    for x,l in [(0,"0%"),(.5,"50%"),(1,"100%")]:
        ax.text(x,-.42,l,ha="center",va="top",fontsize=7,color="#888")
    plt.tight_layout(pad=0); return fig

def plot_comparison(all_res):
    names  = [r[0] for r in all_res]
    probs  = [r[2][1]*100 for r in all_res]
    colors = ["#27ae60" if p>=50 else "#e74c3c" for p in probs]
    fig,ax = plt.subplots(figsize=(6,3)); fig.patch.set_color("#ffffff")
    bars   = ax.bar(names,probs,color=colors,edgecolor="white",linewidth=1.5,width=.5)
    for b,v in zip(bars,probs):
        ax.text(b.get_x()+b.get_width()/2,b.get_height()+1.5,f"{v:.1f}%",
                ha="center",fontweight="700",fontsize=11)
    ax.axhline(50,color="#1a3a5c",linestyle="--",linewidth=1.2,alpha=.6)
    ax.set_ylim(0,115); ax.set_ylabel("On-Time Prob (%)",fontsize=9,color="#5d6d7e")
    ax.set_title("All 3 Models Compared",fontsize=12,fontweight="bold",color="#1a3a5c")
    ax.tick_params(axis="x",labelsize=8)
    for sp in ["top","right"]: ax.spines[sp].set_visible(False)
    plt.tight_layout(); return fig

def plot_fi(sys_dict, features):
    rf    = sys_dict['Random Forest']
    imps  = rf.feature_importances_
    lbls  = [FEATURE_LABELS.get(f,f) for f in features]
    pairs = sorted(zip(imps,lbls))
    iv,lv = zip(*pairs)
    clrs  = ["#e8b84b" if i>=len(features)-3 else "#a8c0d6" for i in range(len(features))]
    fig,ax= plt.subplots(figsize=(7,max(4,len(features)*.38))); fig.patch.set_color("#ffffff")
    ax.barh(lv,iv,color=clrs,edgecolor="white",linewidth=.8)
    for i,(l,v) in enumerate(zip(lv,iv)):
        ax.text(v+.001,i,f"{v:.4f}",va="center",fontsize=7,color="#5d6d7e")
    ax.legend(handles=[mpatches.Patch(color="#e8b84b",label="Top 3"),
                        mpatches.Patch(color="#a8c0d6",label="Others")],fontsize=8,loc="lower right")
    ax.set_xlabel("Importance",fontsize=9); ax.set_title("RF Feature Importance",fontsize=11,fontweight="bold",color="#1a3a5c")
    ax.tick_params(axis="y",labelsize=7.5)
    for sp in ["top","right"]: ax.spines[sp].set_visible(False)
    plt.tight_layout(); return fig

# ─────────────────────────────────────────────────────────────
# RESULT BLOCK
# ─────────────────────────────────────────────────────────────
def show_results(label, probs, all_res, sys_dict, features):
    po = probs[1]*100; pd_ = probs[0]*100
    if label==1:
        st.markdown(f'<div class="result-ontime"><div class="result-icon">✅</div><p class="result-label">ON-TIME GRADUATION</p><p class="result-sub">Confidence: <strong>{po:.1f}%</strong></p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-delayed"><div class="result-icon">⚠️</div><p class="result-label">DELAYED GRADUATION</p><p class="result-sub">Confidence: <strong>{pd_:.1f}%</strong></p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-card"><span class="section-title">📈 Probability Breakdown</span>', unsafe_allow_html=True)
    ca,cb = st.columns(2); ca.metric("✅ On-Time",f"{po:.1f}%"); cb.metric("⚠️ Delayed",f"{pd_:.1f}%")
    st.pyplot(plot_gauge(probs[1]),use_container_width=True); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><span class="section-title">💡 Risk Interpretation</span>', unsafe_allow_html=True)
    if po>=70:   st.markdown("🟢 **Low Risk** — Strong on-time indicators. Continue monitoring each semester.")
    elif po>=45: st.markdown("🟡 **Moderate Risk** — Borderline. Recommend proactive academic advising.")
    else:        st.markdown("🔴 **High Risk** — Immediate academic intervention recommended.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><span class="section-title">🤖 All Models Compared</span>', unsafe_allow_html=True)
    st.pyplot(plot_comparison(all_res),use_container_width=True); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><span class="section-title">📊 Feature Importance (RF)</span>', unsafe_allow_html=True)
    st.pyplot(plot_fi(sys_dict,features),use_container_width=True); plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SASE TOTAL DISPLAY HELPER
# ─────────────────────────────────────────────────────────────
def show_sase_total(ma, la, sci, ap):
    """Display auto-computed Total SASE as a styled read-only box."""
    total = ma + la + sci + ap
    st.markdown(
        f"""
        <div class="sase-total-box">
            <div class="label">Total SASE (Auto-Computed)</div>
            <div class="value">{total:.0f}</div>
            <div class="hint">Math ({ma:.0f}) + Language Arts ({la:.0f}) + Science ({sci:.0f}) + Abstract/Perceptual ({ap:.0f})</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return float(total)

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    all_models, missing = load_models()

    st.markdown("""
    <div class="hero">
        <div class="badge">Thesis Project · Civil Engineering</div>
        <h1>🎓 CE Graduation Predictor</h1>
        <p>Predicting On-Time Graduation of Civil Engineering Students using Machine Learning</p>
    </div>""", unsafe_allow_html=True)

    if all_models is None:
        st.error(f"""
        ### ⚠️ Missing files: `{', '.join(missing)}`

        Add this at the end of your **v2 notebook** and run it:
        ```python
        import joblib
        joblib.dump(models_A['Random Forest'],       'model_A_rf.pkl')
        joblib.dump(models_A['Logistic Regression'], 'model_A_lr.pkl')
        joblib.dump(models_A['Decision Tree'],       'model_A_dt.pkl')
        joblib.dump(imp_a, 'imputer_A.pkl')
        joblib.dump(scl_a, 'scaler_A.pkl')
        joblib.dump(models_B['Random Forest'],       'model_B_rf.pkl')
        joblib.dump(models_B['Logistic Regression'], 'model_B_lr.pkl')
        joblib.dump(models_B['Decision Tree'],       'model_B_dt.pkl')
        joblib.dump(imp_b, 'imputer_B.pkl')
        joblib.dump(scl_b, 'scaler_B.pkl')
        print("✅ All 10 files saved!")
        ```
        Copy all **10 `.pkl` files** into the **`model/`** subfolder (i.e. `ce_graduation/model/`), then refresh.
        """)
        st.stop()

    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        chosen_model = st.selectbox("Prediction Model", MODEL_ORDER)
        st.markdown("---")
        st.markdown("""
        **📘 Philippine Grading Scale**

        | Grade | Meaning |
        |---|---|
        | 1.0 | Excellent |
        | 1.5 | Very Good |
        | 2.0 | Good |
        | 2.5 | Satisfactory |
        | 3.0 | Lowest Passing |
        | 5.0 | Failed |
        """)
        st.markdown("----")
        st.caption("Decision-support tool only. Always combine with human judgment.")

    tab_a, tab_b = st.tabs([
        "🎓 System A — Incoming Freshmen (SASE Only)",
        "📚 System B — All Year Levels (Full Profile)",
    ])

    # ── SYSTEM A ──────────────────────────────────────────────
    with tab_a:
        st.info("**System A** uses only SASE scores. Best used at **admission or orientation** — before any university subjects are taken.")
        cin, cout = st.columns([1.1,.9], gap="large")
        with cin:
            st.markdown('<div class="section-card"><span class="section-title">📝 SASE Scores</span>', unsafe_allow_html=True)
            st.markdown('<div class="grade-note">From the student\'s admission records. Total SASE is automatically computed from the four sub-scores.</div>', unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1:
                ma_a  = st.number_input("Mathematics",      min_value=0.0, max_value=80.0,  value=20.0, step=1.0, key="a_ma")
                sci_a = st.number_input("Science",          min_value=0.0, max_value=60.0,  value=10.0, step=1.0, key="a_sci")
            with c2:
                la_a  = st.number_input("Language Arts",    min_value=0.0, max_value=80.0,  value=35.0, step=1.0, key="a_la")
                ap_a  = st.number_input("Abstract/Perceptual", min_value=0.0, max_value=60.0, value=15.0, step=1.0, key="a_ap")
            # Auto-computed Total SASE (read-only display)
            gs_a = show_sase_total(ma_a, la_a, sci_a, ap_a)
            st.markdown('</div>', unsafe_allow_html=True)
            btn_a = st.button("🔍 Predict (System A)", key="btn_a")
        with cout:
            if not btn_a:
                st.markdown('<div style="background:#eaf2fb;border-radius:14px;padding:40px 28px;text-align:center;margin-top:4px;"><div style="font-size:3rem">📋</div><h3 style="color:#1a3a5c;margin:8px 0">System A Ready</h3><p style="color:#5d6d7e;font-size:.9rem">Enter SASE scores and click Predict.</p></div>', unsafe_allow_html=True)
            else:
                inp_a = {'SASE_GS':gs_a,'SASE_MA':ma_a,'SASE_LA':la_a,'SASE_SCI':sci_a,'SASE_AP':ap_a}
                lbl,prb   = run_prediction(all_models['A'], inp_a, FEATURES_A, chosen_model)
                all_res_a = run_all_models(all_models['A'], inp_a, FEATURES_A)
                show_results(lbl, prb, all_res_a, all_models['A'], FEATURES_A)

    # ── SYSTEM B ──────────────────────────────────────────────
    with tab_b:
        st.info("**System B** uses the full academic profile. Best used **each semester** after new grades are available.")
        cin2, cout2 = st.columns([1.1,.9], gap="large")
        with cin2:
            # SASE
            st.markdown('<div class="section-card"><span class="section-title">📝 SASE Scores</span>', unsafe_allow_html=True)
            st.markdown('<div class="grade-note">Total SASE is automatically computed from the four sub-scores.</div>', unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1:
                ma_b  = st.number_input("Mathematics",   min_value=0.0, max_value=80.0,  value=20.0, step=1.0, key="b_ma")
                sci_b = st.number_input("Science",       min_value=0.0, max_value=60.0,  value=10.0, step=1.0, key="b_sci")
            with c2:
                la_b  = st.number_input("Language Arts", min_value=0.0, max_value=80.0,  value=35.0, step=1.0, key="b_la")
                ap_b  = st.number_input("Abstract/Perceptual", min_value=0.0, max_value=60.0, value=15.0, step=1.0, key="b_ap")
            # Auto-computed Total SASE (read-only display)
            gs_b = show_sase_total(ma_b, la_b, sci_b, ap_b)
            st.markdown('</div>', unsafe_allow_html=True)

            # Grades
            st.markdown('<div class="section-card"><span class="section-title">📚 Subject Grades</span>', unsafe_allow_html=True)
            st.markdown('<div class="grade-note">⚠️ 1.0 = Best, 3.0 = Lowest Passing. For subjects not yet taken, uncheck the box — the model will handle missing values automatically.</div>', unsafe_allow_html=True)
            c3,c4 = st.columns(2)
            with c3:
                mat060 = st.number_input("MAT060",  min_value=1.0, max_value=5.0, value=2.25, step=.25, format="%.2f", key="m60")
                mat070 = st.number_input("MAT070",  min_value=1.0, max_value=5.0, value=2.50, step=.25, format="%.2f", key="m70")
                ens161 = st.number_input("ENS161",  min_value=1.0, max_value=5.0, value=2.75, step=.25, format="%.2f", key="e161")
                cve151 = st.number_input("CVE151",  min_value=1.0, max_value=5.0, value=3.00, step=.25, format="%.2f", key="c151")
                cve155 = st.number_input("CVE155",  min_value=1.0, max_value=5.0, value=2.50, step=.25, format="%.2f", key="c155")
                cve161 = st.number_input("CVE161",  min_value=1.0, max_value=5.0, value=2.25, step=.25, format="%.2f", key="c161")
            with c4:
                t195 = st.checkbox("CVE195 taken?", key="t195")
                cve195 = st.number_input("CVE195", min_value=1.0, max_value=5.0, value=2.0, step=.25, format="%.2f", key="c195", disabled=not t195)
                t196 = st.checkbox("CVE196 taken?", key="t196")
                cve196 = st.number_input("CVE196", min_value=1.0, max_value=5.0, value=2.0, step=.25, format="%.2f", key="c196", disabled=not t196)
                t111 = st.checkbox("CVE111 taken?", key="t111")
                cve111 = st.number_input("CVE111", min_value=1.0, max_value=5.0, value=2.0, step=.25, format="%.2f", key="c111", disabled=not t111)
                t112 = st.checkbox("CVE112 taken?", key="t112")
                cve112 = st.number_input("CVE112", min_value=1.0, max_value=5.0, value=2.0, step=.25, format="%.2f", key="c112", disabled=not t112)
            st.markdown('</div>', unsafe_allow_html=True)

            # Academic Standing + engineered features
            st.markdown('<div class="section-card"><span class="section-title">📊 Academic Standing & Struggle Indicators (NEW in v2)</span>', unsafe_allow_html=True)
            cgpa = st.slider("CGPA", min_value=1.0, max_value=3.0, value=2.40, step=.01, format="%.2f")
            c5,c6 = st.columns(2)
            with c5:
                total_retakes = st.number_input("Total Retakes",      min_value=0, max_value=30, value=2, step=1, help="Total extra subject attempts across all subjects")
                avg_grade     = st.number_input("Average Grade",      min_value=1.0, max_value=5.0, value=2.54, step=.01, format="%.2f")
            with c6:
                max_retake    = st.number_input("Max Single Retake",  min_value=0, max_value=10, value=1, step=1, help="Worst single subject: how many extra attempts?")
                hard_fails    = st.number_input("Hard Fails (3.00)",  min_value=0, max_value=20, value=1, step=1, help="Number of subjects where grade = exactly 3.00")
            st.markdown('</div>', unsafe_allow_html=True)

            btn_b = st.button("🔍 Predict (System B)", key="btn_b")

        with cout2:
            if not btn_b:
                st.markdown('<div style="background:#eafaf1;border-radius:14px;padding:40px 28px;text-align:center;margin-top:4px;"><div style="font-size:3rem">📚</div><h3 style="color:#1a5276;margin:8px 0">System B Ready</h3><p style="color:#5d6d7e;font-size:.9rem">Fill in the full profile and click Predict.<br>Best used <strong>each semester</strong>.</p></div>', unsafe_allow_html=True)
            else:
                inp_b = {
                    'SASE_GS':gs_b,'SASE_MA':ma_b,'SASE_LA':la_b,'SASE_SCI':sci_b,'SASE_AP':ap_b,
                    'MAT060':mat060,'MAT070':mat070,'ENS161':ens161,
                    'CVE151':cve151,'CVE155':cve155,'CVE161':cve161,
                    'CVE195':cve195 if t195 else np.nan,
                    'CVE196':cve196 if t196 else np.nan,
                    'CVE111':cve111 if t111 else np.nan,
                    'CVE112':cve112 if t112 else np.nan,
                    'CGPA':cgpa,
                    'TOTAL_RETAKES':float(total_retakes),'MAX_RETAKE':float(max_retake),
                    'AVG_GRADE':avg_grade,'HARD_FAILS':float(hard_fails),
                }
                lbl,prb   = run_prediction(all_models['B'], inp_b, FEATURES_B, chosen_model)
                all_res_b = run_all_models(all_models['B'], inp_b, FEATURES_B)
                show_results(lbl, prb, all_res_b, all_models['B'], FEATURES_B)
                

if __name__ == "__main__":
    main()
