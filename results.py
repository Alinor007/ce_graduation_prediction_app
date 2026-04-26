"""
results.py
Renders prediction results: banner, probability breakdown,
risk interpretation, algorithm comparison, and feature importance.
"""

import matplotlib.pyplot as plt
import streamlit as st

import charts
from layout import card_open, card_close
from predictor import AlgorithmResult, PredictionResult, get_feature_importances
from styles import RESULT_HTML, PLACEHOLDER_HTML


# ── Public API ─────────────────────────────────────────────────

def render_results(
    result: PredictionResult,
    algo_results: list[AlgorithmResult],
    model_bundle: dict,
    features: list[str],
) -> None:
    """Render the complete result panel after a prediction."""
    _render_result_banner(result)
    _render_probability_section(result)
    _render_risk_section(result)
    _render_comparison_section(algo_results)
    _render_importance_section(model_bundle, features)


def render_placeholder(bg: str, icon: str, color: str, title: str, body: str) -> None:
    """Render an empty-state placeholder card."""
    st.markdown(
        PLACEHOLDER_HTML.format(icon=icon, color=color, title=title, body=body),
        unsafe_allow_html=True,
    )


def plt_close() -> None:
    """Close the current matplotlib figure to free memory."""
    plt.close()


# ── Private helpers ────────────────────────────────────────────

def _render_result_banner(result: PredictionResult) -> None:
    if result.is_ontime:
        html = RESULT_HTML.format(
            css_class="ce-result-ontime",
            icon="✅",
            label="ON-TIME GRADUATION",
            confidence=result.prob_ontime * 100,
        )
    else:
        html = RESULT_HTML.format(
            css_class="ce-result-delayed",
            icon="⚠️",
            label="DELAYED GRADUATION",
            confidence=result.prob_delayed * 100,
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
