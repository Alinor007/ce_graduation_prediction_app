"""
layout.py
Page-level rendering: navbar, hero, model cards, sidebar, section cards.
All functions accept no domain data — they only deal with page structure.
"""

import streamlit as st

from styles import CSS, NAVBAR_HTML, HERO_HTML, MODELS_OVERVIEW_HTML


def inject_css() -> None:
    """Inject design-system CSS + fixed navbar into the page."""
    st.markdown(CSS + NAVBAR_HTML, unsafe_allow_html=True)


def render_hero() -> None:
    """Full-width hero banner."""
    st.markdown(HERO_HTML, unsafe_allow_html=True)


def render_models_overview() -> None:
    """Three clickable model summary cards above the tabs."""
    st.markdown(MODELS_OVERVIEW_HTML, unsafe_allow_html=True)


def render_sidebar(algorithms: list[str]) -> str:
    """Sidebar settings panel; returns the selected algorithm name."""
    with st.sidebar:
        st.markdown("## Settings")
        chosen = st.selectbox("Algorithm", algorithms, label_visibility="visible")
        st.markdown("---")
        st.markdown("""
**📐 Model Guide**

| Model | Category |
|---|---|
| **Model 1** | Adminssion Profile |
| **Model 2** | Academic Program |
| **Model 3** | Integrated Assessment |
""")
        st.markdown("---")
        st.caption("Decision-support only. Always combine with human judgment.")
    return chosen


def card_open(title: str) -> None:
    """Open a styled section card. Title format: 'emoji text'."""
    parts = title.split(" ", 1)
    icon = parts[0] if len(parts) > 0 else "📄"
    text = parts[1] if len(parts) > 1 else title
    st.markdown(
        f'''<div class="ce-card">
              <div class="ce-card-hd">
                <div class="ce-card-icon">{icon}</div>
                <span class="ce-card-title">{text}</span>
              </div>''',
        unsafe_allow_html=True,
    )


def card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def grade_note(text: str) -> None:
    st.markdown(
        f'<div class="ce-note"><span>💡</span><span>{text}</span></div>',
        unsafe_allow_html=True,
    )
