
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

    
def detect_skill(text):
    text = text.lower()

    skill_keywords = {
        "acceleration-time graphs": [
            "acceleration-time",
            "acceleration time graph",
            "acceleration vs time",
            "a-t graph"
        ],
        "velocity-time graphs": [
            "velocity-time",
            "velocity time graph",
            "velocity vs time",
            "v-t graph"
        ],
        "position-time graphs": [
            "position-time",
            "displacement-time",
            "position time graph",
            "x-t graph"
        ],
        "projectile motion": [
            "projectile",
            "launch angle",
            "horizontal range"
        ],
        "uniform acceleration": [
            "uniform acceleration",
            "constant acceleration",
            "suvat"
        ]
    }

    for skill, keywords in skill_keywords.items():
        if any(keyword in text for keyword in keywords):
            return skill

    return None
