
import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "problem_catalog.json"


def find_similar_problems(topic, level="SL", skills=None, limit=3):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    skills = skills or []
    results = []

    for problem in catalog["problems"]:
        # SL students receive SL-compatible problems.
        # HL students may receive both SL and HL problems.
        allowed = ["SL"] if level == "SL" else ["SL", "HL"]

        if problem["level"] not in allowed:
            continue

        score = 0

        if problem["topic"].lower() == topic.lower():
            score += 5

        for skill in skills:
            if skill.lower() in [
                s.lower() for s in problem.get("skills", [])
            ]:
                score += 2

        if score > 0:
            results.append((score, problem))

    results.sort(key=lambda x: x[0], reverse=True)

    return [problem for score, problem in results[:limit]]



def detect_topic(text):
    text = text.lower()

    topic_keywords = {
        "A.1 Kinematics": [
            "velocity", "acceleration", "displacement",
            "kinematics", "free fall", "projectile",
            "speed", "position-time", "velocity-time",
            "ускорение", "скорость"
        ],
        "A.2 Forces and momentum": [
            "force", "momentum", "impulse",
            "newton", "collision", "friction",
            "сила", "импульс"
        ],
        "A.3 Work, energy and power": [
            "work", "kinetic energy", "potential energy",
            "power", "conservation of energy",
            "работа", "энергия"
        ],
        "A.4 Rigid body mechanics": [
            "torque", "moment of inertia",
            "angular acceleration", "rotation",
            "вращение", "момент силы"
        ]
    }

    for topic, keywords in topic_keywords.items():
        if any(keyword in text for keyword in keywords):
            return topic

    return None
