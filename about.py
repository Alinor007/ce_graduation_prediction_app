"""
about.py
Renders the About page: thesis card, authors, adviser, and institution.
Self-contained — no shared state or inputs needed.
"""

import streamlit as st

import base64 
import pathlib 

def render_about_page() -> None:
    # Hero banner
    st.markdown("""
<div class="ce-about-hero fade-up">
  <span class="ce-about-tag">Undergraduate Thesis · January 2026</span>
  <h2 class="ce-about-title">About This Project</h2>
  <div class="ce-about-line"></div>
  <p class="ce-about-desc">Mindanao State University – Main Campus, Marawi City · Civil Engineering Department</p>
</div>
""", unsafe_allow_html=True)

    # Thesis card
    st.markdown("""
<div class="ce-thesis-card fade-up delay-1">
  <div class="ce-thesis-eye"> Thesis Title</div>
  <div class="ce-thesis-title">
    A Predictive Analytics Study on the Key Determinants of On-Time Completion
    of Civil Engineering Students at MSU–Marawi
  </div>
  <p class="ce-thesis-body">
    An undergraduate thesis presented to the Faculty of the Civil Engineering Department,
    College of Engineering, in partial fulfillment of the requirements for the degree of
    <span class="ce-thesis-hl">Bachelor of Science in Civil Engineering</span>.
  </p>
</div>
""", unsafe_allow_html=True)

    # Authors
    st.markdown('<div class="ce-section-hd">Authors</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    authors = [
        ("Bilao, Jonaif H.",         "BS Civil Engineering", "JB"),
        ("Dibaratun, Norhan L.",      "BS Civil Engineering", "ND"),
        ("Villamor, Airene Grace L.", "BS Civil Engineering", "AV"),

    ]
    for col, (name, degree, init) in zip([col1, col2, col3], authors):
        with col:
            st.markdown(f"""
<div class="ce-person-card fade-up delay-2">
  <div class="ce-avatar">{init}</div>
  <div class="ce-person-name">{name}</div>
  <span class="ce-person-role">Author</span>
  <div class="ce-person-detail">{degree}</div>
</div>
""", unsafe_allow_html=True)

    # Adviser
    st.markdown('<div class="ce-section-hd">Thesis Adviser</div>', unsafe_allow_html=True)
    _, adv_col, _ = st.columns([1, 2, 1])

    def _img_b64(path: str) -> str:
        data = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
        return f"data:image/png;base64,{data}"

    adv_photo = pathlib.Path("pictures/profiles/adviser.png")
    if adv_photo.exists():
        adv_avatar = f'<img src="{_img_b64(str(adv_photo))}"  class="ce-avatar adv" style="object-fit:cover; width:150px; height:150px;" />'
    else:
        adv_avatar = '<div class="ce-avatar adv">ND</div>'

    with adv_col:
        st.markdown(f"""
    <div class="ce-person-card adviser fade-up delay-3" >
      {adv_avatar}
      <div class="ce-person-name">Engr. Nhour R. Dibangkitun</div>
      <span class="ce-person-role">Thesis Adviser</span>
      <div class="ce-person-detail">
        Civil Engineering Department<br>
        College of Engineering<br>
        Mindanao State University – Main Campus
      </div>
    </div>
""", unsafe_allow_html=True)

    # Institution
    st.markdown('<div class="ce-section-hd">Institution</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="ce-institution fade-up delay-4">
  <div class="ce-inst-name">Mindanao State University – Main Campus</div>
  <div class="ce-inst-sub">
    College of Engineering | Civil Engineering Department<br>
    Marawi City, Lanao del Sur, Philippines
  </div>
  <div class="ce-inst-tags">
    <span class="ce-inst-tag">🎓 BSCE Program</span>
    <span class="ce-inst-tag">📅 2018 Curriculum</span>
    <span class="ce-inst-tag">📌 January 2026</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # Footer
    st.markdown("""
<div class="ce-footer">
  CE Graduation Predictor · Mindanao State University – Marawi · 2026<br>
  <em>Decision-support tool only. Always combine with human judgment.</em>
</div>
""", unsafe_allow_html=True)
