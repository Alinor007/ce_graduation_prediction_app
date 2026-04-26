"""
ui_components.py
Facade — re-exports everything that tabs.py and app.py import.
No logic lives here. Add new functions to the appropriate module instead.
"""

from about import render_about_page
from inputs import (
    academic_standing_inputs,
    grade_inputs,
    sase_inputs,
    shs_inputs,
)
from layout import (
    card_close,
    card_open,
    grade_note,
    inject_css,
    render_hero,
    render_models_overview,
    render_sidebar,
)
from results import plt_close, render_placeholder, render_results
