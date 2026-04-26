"""
tabs.py
One function per tab. Each function collects inputs, runs prediction,
and delegates rendering to ui_components. No business logic lives here.
"""

import streamlit as st

import ui_components as ui
from config import FEATURES
from predictor import predict, predict_all_algorithms


def _strand_to_onehot(strand: str) -> dict[str, int]:
    """Convert a strand name to a one-hot encoded dict matching STRAND_COLS."""
    strands = ["ABM", "GAS", "HUMSS", "ICT", "SPORTS", "STEM", "TVL"]
    return {f"STRAND_{s}": (1 if s == strand else 0) for s in strands}


# ── Tab 1: Pre-Admission ──────────────────────────────────────

def render_model1_tab(all_models: dict, algorithm: str) -> None:
    st.info(
        "**Model 1** uses pre-admission data only. "
        "Best used at **admission or orientation** — before any university subjects are taken."
    )
    col_inputs, col_results = st.columns([1.1, 0.9], gap="large")

    with col_inputs:
        ui.card_open("📝 SASE Scores")
        gs, ma, la, sci, ap = ui.sase_inputs("m1")
        ui.card_close()

        ui.card_open("🏫 SHS Background")
        gwa_num, strand = ui.shs_inputs("m1")
        ui.card_close()

        predict_clicked = st.button("🔍 Predict — Model 1", key="btn_1")

    with col_results:
        if not predict_clicked:
            ui.render_placeholder(
                bg="#eaf2fb", icon="📋", color="#1a3a5c",
                title="Model 1 Ready",
                body="Enter SASE scores + SHS background and click Predict.",
            )
            return

        inputs = {
            "SASE_GS": gs, "SASE_MA": ma, "SASE_LA": la,
            "SASE_SCI": sci, "SASE_AP": ap,
            "SHS_GWA_NUM": gwa_num,
            **_strand_to_onehot(strand),
        }
        bundle  = all_models["1"]
        features = FEATURES["1"]
        result       = predict(bundle, inputs, features, algorithm)
        algo_results = predict_all_algorithms(bundle, inputs, features)
        ui.render_results(result, algo_results, bundle, features)


# ── Tab 2: In-Program ─────────────────────────────────────────

def render_model2_tab(all_models: dict, algorithm: str) -> None:
    st.info(
        "**Model 2** uses in-program academic data. "
        "Best used **each semester** after new grades are posted."
    )
    col_inputs, col_results = st.columns([1.1, 0.9], gap="large")

    with col_inputs:
        ui.card_open("📚 Subject Grades")
        grades = ui.grade_inputs("m2")
        ui.card_close()

        ui.card_open("📊 Academic Standing")
        cgpa, total_ret, max_ret, avg_grade, hard_fails = ui.academic_standing_inputs("m2", grades)
        ui.card_close()

        predict_clicked = st.button("🔍 Predict — Model 2", key="btn_2")

    with col_results:
        if not predict_clicked:
            ui.render_placeholder(
                bg="#eafaf1", icon="📚", color="#1a5276",
                title="Model 2 Ready",
                body="Fill in grades + academic standing and click Predict.<br>Best used <strong>each semester</strong>.",
            )
            return

        inputs = {
            **grades,
            "CGPA":          cgpa,
            "TOTAL_RETAKES": total_ret,
            "MAX_RETAKE":    max_ret,
            "AVG_GRADE":     avg_grade,
            "HARD_FAILS":    hard_fails,
        }
        bundle   = all_models["2"]
        features = FEATURES["2"]
        result       = predict(bundle, inputs, features, algorithm)
        algo_results = predict_all_algorithms(bundle, inputs, features)
        ui.render_results(result, algo_results, bundle, features)


# ── Tab 3: Combined ───────────────────────────────────────────

def render_model3_tab(all_models: dict, algorithm: str) -> None:
    st.info(
        "**Model 3** combines pre-admission and in-program data "
        "for the most comprehensive risk profile. Use when **all data is available**."
    )
    col_inputs, col_results = st.columns([1.1, 0.9], gap="large")

    with col_inputs:
        ui.card_open("📝 SASE Scores")
        gs, ma, la, sci, ap = ui.sase_inputs("m3")
        ui.card_close()

        ui.card_open("🏫 SHS Background")
        gwa_num, strand = ui.shs_inputs("m3")
        ui.card_close()

        ui.card_open("📚 Subject Grades")
        grades = ui.grade_inputs("m3")
        ui.card_close()

        ui.card_open("📊 Academic Standing")
        cgpa, total_ret, max_ret, avg_grade, hard_fails = ui.academic_standing_inputs("m3", grades)
        ui.card_close()

        predict_clicked = st.button("🔍 Predict — Model 3", key="btn_3")

    with col_results:
        if not predict_clicked:
            ui.render_placeholder(
                bg="#fef9e7", icon="🔬", color="#7d6608",
                title="Model 3 Ready",
                body="Fill in the complete profile and click Predict.<br>Uses <strong>all available features</strong>.",
            )
            return

        inputs = {
            "SASE_GS": gs, "SASE_MA": ma, "SASE_LA": la,
            "SASE_SCI": sci, "SASE_AP": ap,
            "SHS_GWA_NUM": gwa_num,
            **_strand_to_onehot(strand),
            **grades,
            "CGPA":          cgpa,
            "TOTAL_RETAKES": total_ret,
            "MAX_RETAKE":    max_ret,
            "AVG_GRADE":     avg_grade,
            "HARD_FAILS":    hard_fails,
        }
        bundle   = all_models["3"]
        features = FEATURES["3"]
        result       = predict(bundle, inputs, features, algorithm)
        algo_results = predict_all_algorithms(bundle, inputs, features)
        ui.render_results(result, algo_results, bundle, features)
