"""
charts.py
All matplotlib figure builders.
Each function returns a Figure — callers decide how to render it.
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from predictor import AlgorithmResult


# ── Colour palette ────────────────────────────────────────────
GREEN  = "#27ae60"
RED    = "#e74c3c"
NAVY   = "#1a3a5c"
GOLD   = "#e8b84b"
MUTED  = "#a8c0d6"
GRAY   = "#dce3ed"
TEXT   = "#5d6d7e"


def gauge(prob_ontime: float) -> plt.Figure:
    """Horizontal bar showing on-time probability vs 50 % threshold."""
    fig, ax = plt.subplots(figsize=(5, 0.65))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.barh(0, 1, color=GRAY, height=0.5)
    ax.barh(0, prob_ontime, color=GREEN if prob_ontime >= 0.5 else RED, height=0.5)
    ax.axvline(0.5, color=NAVY, linewidth=1.5, linestyle="--", alpha=0.6)

    for x, label in [(0, "0%"), (0.5, "50%"), (1, "100%")]:
        ax.text(x, -0.42, label, ha="center", va="top", fontsize=7, color="#888")

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, 0.5)
    ax.axis("off")
    plt.tight_layout(pad=0)
    return fig


def algorithm_comparison(results: list[AlgorithmResult]) -> plt.Figure:
    """Bar chart comparing on-time probability across all algorithms."""
    names  = [r.name for r in results]
    values = [r.result.prob_ontime * 100 for r in results]
    colors = [GREEN if v >= 50 else RED for v in values]

    fig, ax = plt.subplots(figsize=(6, 3))
    fig.patch.set_color("#ffffff")

    bars = ax.bar(names, values, color=colors, edgecolor="white", linewidth=1.5, width=0.45)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{value:.1f}%",
            ha="center",
            fontweight="bold",
            fontsize=11,
        )

    ax.axhline(50, color=NAVY, linestyle="--", linewidth=1.2, alpha=0.6)
    ax.set_ylim(0, 115)
    ax.set_ylabel("On-Time Probability (%)", fontsize=9, color=TEXT)
    ax.set_title("Algorithm Comparison", fontsize=12, fontweight="bold", color=NAVY)
    ax.tick_params(axis="x", labelsize=9)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig


def feature_importance(importance_pairs: list[tuple[str, float]]) -> plt.Figure:
    """Horizontal bar chart of Random Forest feature importances."""
    labels, values = zip(*importance_pairs)
    n = len(labels)
    colors = [GOLD if i >= n - 3 else MUTED for i in range(n)]

    fig, ax = plt.subplots(figsize=(7, max(4, n * 0.38)))
    fig.patch.set_color("#ffffff")

    ax.barh(labels, values, color=colors, edgecolor="white", linewidth=0.8)

    for i, (label, value) in enumerate(zip(labels, values)):
        ax.text(value + 0.001, i, f"{value:.4f}", va="center", fontsize=7, color=TEXT)

    ax.legend(
        handles=[
            mpatches.Patch(color=GOLD, label="Top 3"),
            mpatches.Patch(color=MUTED, label="Others"),
        ],
        fontsize=8,
        loc="lower right",
    )
    ax.set_xlabel("Importance", fontsize=9)
    ax.set_title("RF Feature Importance", fontsize=11, fontweight="bold", color=NAVY)
    ax.tick_params(axis="y", labelsize=7.5)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig
