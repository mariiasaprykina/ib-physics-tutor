
# ==========================================
# OFFICIAL IB PHYSICS CURRICULUM DATA
# First assessment 2025
# ==========================================

BRIEF_URL = (
    "https://ibo.org/globalassets/new-structure/"
    "recognition/pdfs/"
    "dp_sciences_physics_subject-brief_jan_2022_e.pdf"
)

SOURCE = (
    "International Baccalaureate Organization. "
    "Diploma Programme Subject Brief: Sciences — "
    "Physics. 2022. First assessment 2025."
)


# ==========================================
# COURSE OVERVIEW
# ==========================================

COURSE = {
    "SL": {
        "teaching_hours": 150,
        "syllabus_hours": 110,
        "experimental_hours": 40,
        "exam_hours": 3,
        "topics": 19,
        "practical_work": 20,
        "collaborative_project": 10,
        "investigation": 10,
    },

    "HL": {
        "teaching_hours": 240,
        "syllabus_hours": 180,
        "experimental_hours": 60,
        "exam_hours": 4.5,
        "topics": 24,
        "practical_work": 40,
        "collaborative_project": 10,
        "investigation": 10,
    },
}


# ==========================================
# ASSESSMENT STRUCTURE
# ==========================================

ASSESSMENT = [

    {
        "id": "paper1",
        "title": "Paper 1",
        "weight": 36,
        "duration": {
            "SL": 90,
            "HL": 120,
        },
        "type": "external",
        "parts": [
            "Paper 1A",
            "Paper 1B",
        ],
    },

    {
        "id": "paper2",
        "title": "Paper 2",
        "weight": 44,
        "duration": {
            "SL": 90,
            "HL": 150,
        },
        "type": "external",
    },

    {
        "id": "ia",
        "title": "Scientific investigation",
        "weight": 20,
        "duration": {
            "SL": 600,
            "HL": 600,
        },
        "type": "internal",
        "max_words": 3000,
    },

]


# ==========================================
# SYLLABUS
# ==========================================

SYLLABUS = [

    {
        "id": "A",
        "title": "Space, time and motion",
        "hours": {
            "SL": 27,
            "HL": 42,
        },
        "topics": [
            ("A.1", "Kinematics", "both"),
            ("A.2", "Forces and momentum", "both"),
            ("A.3", "Work, energy and power", "both"),
            ("A.4", "Rigid body mechanics", "hl"),
            ("A.5", "Galilean and special relativity", "hl"),
        ],
    },

    {
        "id": "B",
        "title": "The particulate nature of matter",
        "hours": {
            "SL": 24,
            "HL": 32,
        },
        "topics": [
            ("B.1", "Thermal energy transfers", "both"),
            ("B.2", "Greenhouse effect", "both"),
            ("B.3", "Gas laws", "both"),
            ("B.4", "Thermodynamics", "hl"),
            ("B.5", "Current and circuits", "both"),
        ],
    },

    {
        "id": "C",
        "title": "Wave behaviour",
        "hours": {
            "SL": 17,
            "HL": 29,
        },
        "topics": [
            ("C.1", "Simple harmonic motion", "both_hl"),
            ("C.2", "Wave model", "both"),
            ("C.3", "Wave phenomena", "both_hl"),
            ("C.4", "Standing waves and resonance", "both"),
            ("C.5", "Doppler effect", "both_hl"),
        ],
    },

    {
        "id": "D",
        "title": "Fields",
        "hours": {
            "SL": 19,
            "HL": 38,
        },
        "topics": [
            ("D.1", "Gravitational fields", "both_hl"),
            ("D.2", "Electric and magnetic fields", "both_hl"),
            ("D.3", "Motion in electromagnetic fields", "both"),
            ("D.4", "Induction", "hl"),
        ],
    },

    {
        "id": "E",
        "title": "Nuclear and quantum physics",
        "hours": {
            "SL": 23,
            "HL": 39,
        },
        "topics": [
            ("E.1", "Structure of the atom", "both_hl"),
            ("E.2", "Quantum physics", "hl"),
            ("E.3", "Radioactive decay", "both_hl"),
            ("E.4", "Fission", "both"),
            ("E.5", "Fusion and stars", "both"),
        ],
    },

]


# ==========================================
# ASSESSMENT OBJECTIVES
# ==========================================

OBJECTIVES = [

    {
        "id": "AO1",
        "title": "Knowledge",
        "description": (
            "Recall physical concepts, terminology "
            "and scientific methods."
        ),
    },

    {
        "id": "AO2",
        "title": "Understanding and application",
        "description": (
            "Apply physical principles, scientific "
            "techniques and knowledge."
        ),
    },

    {
        "id": "AO3",
        "title": "Analysis and evaluation",
        "description": (
            "Interpret data, examine experimental "
            "methods and evaluate scientific evidence."
        ),
    },

    {
        "id": "AO4",
        "title": "Scientific investigation",
        "description": (
            "Use scientific skills to conduct "
            "thoughtful and ethical investigations."
        ),
    },

]


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_topics(level):

    result = []

    for theme in SYLLABUS:

        for code, name, coverage in theme["topics"]:

            if level == "SL" and coverage == "hl":
                continue

            result.append({
                "theme": theme["id"],
                "code": code,
                "name": name,
                "coverage": coverage,
            })

    return result


def get_course(level):

    return COURSE.get(level, COURSE["SL"])
