"""
app.py  —  Entry point
Orchestrates page setup, model loading, sidebar, and tab rendering.
Run with:  streamlit run app.py
"""

import streamlit as st
from PIL import Image

import ui_components as ui
from config import ALGORITHMS, EXPORT_SNIPPET
from model_loader import load_all_models, missing_files
from tabs import render_model1_tab, render_model2_tab, render_model3_tab


def _configure_page() -> None:
    logo = Image.open("pictures/logo/logo.png")
    st.set_page_config(
        page_title="CE Graduation Predictor — MSU Marawi",
        page_icon=logo,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def _show_missing_files_error(missing: list[str]) -> None:
    st.error(f"""
### ⚠️ Missing model files: `{', '.join(missing)}`

Add this export block at the end of your **CE_Graduation_Prediction_v3.ipynb** and run it:

```python
{EXPORT_SNIPPET}
```

Copy the **`model/`** folder next to `app.py`, then refresh this page.
""")


def main() -> None:
    _configure_page()
    ui.inject_css()
    ui.render_hero()

    # Guard: stop early if any .pkl files are missing
    missing = missing_files()
    if missing:
        _show_missing_files_error(missing)
        st.stop()

    all_models = load_all_models()
    algorithm  = ui.render_sidebar(ALGORITHMS)

    tab1, tab2, tab3, tab_about = st.tabs([
        "Admission Profile",
        "Academic Program",
        "Integrated  assessment",
        "About",
    ])

    with tab1:
        render_model1_tab(all_models, algorithm)

    with tab2:
        render_model2_tab(all_models, algorithm)

    with tab3:
        render_model3_tab(all_models, algorithm)

    with tab_about:
        ui.render_about_page()


if __name__ == "__main__":
    main()
