"""
inputs.py
All user-input widget functions: SASE scores, SHS background,
subject grades, and academic standing.
"""

import numpy as np
import streamlit as st

from config import ALL_STRANDS, GRADE_COLS_LEFT, GRADE_COLS_RIGHT, GWA_OPTIONS
from layout import grade_note
from styles import PH_GRADE_OPTIONS, PH_GRADE_LABELS


def sase_inputs(prefix: str) -> tuple[float, float, float, float, float]:
    """Render SASE score inputs and auto-computed total.

    Returns:
        (total, math, language, science, abstract)
    """
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
        f"""<div class="ce-sase-total">
              <div class="ce-sase-lbl">Total SASE Score (Auto-Computed)</div>
              <div class="ce-sase-val">{total:.0f}</div>
              <div class="ce-sase-bk">Math {math:.0f} · Language {lang:.0f} · Science {sci:.0f} · Abstract {abst:.0f}</div>
            </div>""",
        unsafe_allow_html=True,
    )
    return total, math, lang, sci, abst


def shs_inputs(prefix: str) -> tuple[float, str]:
    """Render SHS GWA band and strand selectors.

    Returns:
        (gwa_numeric_midpoint, strand_name)
    """
    gwa_band = st.selectbox(
        "SHS GWA Band", list(GWA_OPTIONS.keys()), index=2, key=f"{prefix}_gwa",
        help="Select the student's Senior High School GWA range",
    )
    gwa_num = GWA_OPTIONS[gwa_band]
    st.caption(f"Encoded as numeric midpoint: **{gwa_num}**")
    strand = st.selectbox("SHS Strand", ALL_STRANDS, key=f"{prefix}_strand")
    return gwa_num, strand


def grade_inputs(prefix: str) -> dict[str, float]:
    """Render subject grade selectors using the PH grading scale.

    Returns:
        dict mapping subject code → grade value (float or NaN if not taken)
    """
    grade_note(
        "Select the grade for each subject. "
        "<strong>Leave as '— Not taken —'</strong> if the subject hasn't been taken — "
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


def academic_standing_inputs(
    prefix: str,
    grades: dict[str, float],
) -> tuple[float, float, float, float, float]:
    """Render CGPA slider and retake/average-grade inputs.

    Auto-suggests average grade and hard fails from the grades dict.

    Returns:
        (cgpa, total_retakes, max_retake, avg_grade, hard_fails)
    """
    cgpa = st.slider(
        "CGPA", min_value=1.0, max_value=3.0, value=2.40,
        step=0.01, format="%.2f", key=f"{prefix}_cgpa",
    )

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
            help="Auto-suggested from grades above; adjust if needed",
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
