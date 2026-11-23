
import streamlit as st

st.title("📘 About the IB Physics Exam")
st.caption(
    "Official IB Physics syllabus — First assessment 2025"
)

BRIEF_URL = (
    "https://ibo.org/globalassets/new-structure/"
    "recognition/pdfs/"
    "dp_sciences_physics_subject-brief_jan_2022_e.pdf"
)

st.link_button(
    "📄 Open Official IB Physics Subject Brief",
    BRIEF_URL
)

st.divider()

level = st.session_state.get("physics_level", "SL")

st.subheader("Exam structure")

if level == "SL":
    st.info("Standard Level — 3 hours of written exams")
else:
    st.info("Higher Level — 4.5 hours of written exams")

exam_data = [
    {
        "Component": "Paper 1A + 1B",
        "Format": "Multiple-choice and data-based questions",
        "Duration": "1 h 30 min" if level == "SL" else "2 h",
        "Weight": "36%"
    },
    {
        "Component": "Paper 2",
        "Format": "Short-answer and extended-response questions",
        "Duration": "1 h 30 min" if level == "SL" else "2 h 30 min",
        "Weight": "44%"
    },
    {
        "Component": "Scientific investigation",
        "Format": "Internal assessment",
        "Duration": "10 h allocated",
        "Weight": "20%"
    }
]

st.dataframe(
    exam_data,
    use_container_width=True,
    hide_index=True
)

st.divider()
st.subheader("Physics syllabus")

st.write(
    "Explore the five main themes of IB Physics. "
    "HL students study all common content, "
    "additional HL content, and HL-only topics."
)

# The third field indicates the syllabus coverage:
# "both" = common SL/HL content
# "both_hl" = SL content plus additional HL content
# "hl" = HL-only topic

syllabus = {
    "A. Space, time and motion": [
        ("A.1", "Kinematics", "both"),
        ("A.2", "Forces and momentum", "both"),
        ("A.3", "Work, energy and power", "both"),
        ("A.4", "Rigid body mechanics", "hl"),
        ("A.5", "Galilean and special relativity", "hl")
    ],
    "B. The particulate nature of matter": [
        ("B.1", "Thermal energy transfers", "both"),
        ("B.2", "Greenhouse effect", "both"),
        ("B.3", "Gas laws", "both"),
        ("B.4", "Thermodynamics", "hl"),
        ("B.5", "Current and circuits", "both")
    ],
    "C. Wave behaviour": [
        ("C.1", "Simple harmonic motion", "both_hl"),
        ("C.2", "Wave model", "both"),
        ("C.3", "Wave phenomena", "both_hl"),
        ("C.4", "Standing waves and resonance", "both"),
        ("C.5", "Doppler effect", "both_hl")
    ],
    "D. Fields": [
        ("D.1", "Gravitational fields", "both_hl"),
        ("D.2", "Electric and magnetic fields", "both_hl"),
        ("D.3", "Motion in electromagnetic fields", "both"),
        ("D.4", "Induction", "hl")
    ],
    "E. Nuclear and quantum physics": [
        ("E.1", "Structure of the atom", "both_hl"),
        ("E.2", "Quantum physics", "hl"),
        ("E.3", "Radioactive decay", "both_hl"),
        ("E.4", "Fission", "both"),
        ("E.5", "Fusion and stars", "both")
    ]
}

for theme, topics in syllabus.items():
    with st.expander(theme, expanded=True):
        for code, name, coverage in topics:

            if level == "SL" and coverage == "hl":
                continue

            if coverage == "hl":
                label = "HL only"
            elif coverage == "both_hl":
                label = "SL + HL extension"
            else:
                label = "SL / HL"

            st.markdown(
                f"**{code} {name}**  \n"
                f":grey[{label}]"
            )

st.divider()

st.subheader("Assessment objectives")

objectives = {
    "AO1 — Knowledge": (
        "Demonstrate knowledge of terminology, "
        "facts, concepts and scientific skills."
    ),
    "AO2 — Understanding and application": (
        "Understand and apply scientific knowledge, "
        "skills, techniques and methodologies."
    ),
    "AO3 — Analysis and evaluation": (
        "Analyse, evaluate and synthesize experimental "
        "procedures, data, trends and predictions."
    ),
    "AO4 — Scientific investigation": (
        "Apply skills necessary to carry out "
        "insightful and ethical investigations."
    )
}

for title, description in objectives.items():
    with st.expander(title):
        st.write(description)

st.caption(
    "Source: International Baccalaureate Organization, "
    "Physics Subject Brief (2022), first assessment 2025."
)
