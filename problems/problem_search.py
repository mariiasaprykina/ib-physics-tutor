
import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "problem_catalog.json"


def find_similar_problems(
    topic,
    level="SL",
    skills=None,
    limit=5,
    exclude_ids=None
):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    skills = [s.lower() for s in (skills or [])]
    exclude_ids = set(exclude_ids or [])
    results = []

    for problem in catalog["problems"]:
        if problem["id"] in exclude_ids:
            continue

        if not problem.get("verified", False):
            continue

        allowed = ["SL"] if level == "SL" else ["SL", "HL"]

        if problem["level"] not in allowed:
            continue

        if problem["topic"].lower() != topic.lower():
            continue

        problem_skills = [
            s.lower() for s in problem.get("skills", [])
        ]

        if skills:
            matches = sum(
                1 for skill in skills
                if skill in problem_skills
            )

            if matches == 0:
                continue

            score = matches * 10
        else:
            score = 1

        results.append((score, problem))

    results.sort(key=lambda x: x[0], reverse=True)

    return [p for score, p in results[:limit]]


def detect_topic(text):
    text = text.lower()

    topic_keywords = {
        "A.1 Kinematics": [
            "kinematics",
            "velocity",
            "acceleration",
            "displacement",
            "position-time",
            "velocity-time",
            "acceleration-time",
            "projectile",
            "free fall"
        ],
        "A.2 Forces and momentum": [
            "force",
            "momentum",
            "impulse",
            "newton",
            "collision",
            "friction"
        ],
        "A.3 Work, energy and power": [
            "kinetic energy",
            "potential energy",
            "work done",
            "power",
            "conservation of energy"
        ],
        "A.4 Rigid body mechanics": [
            "torque",
            "moment of inertia",
            "angular acceleration",
            "rotation"
        ]
    }

    for topic, keywords in topic_keywords.items():
        if any(keyword in text for keyword in keywords):
            return topic

    return None


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
