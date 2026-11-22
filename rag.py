
from pathlib import Path
import re

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


def retrieve_knowledge(query, max_results=3):
    """Find relevant sections in local knowledge files."""

    if not KNOWLEDGE_DIR.exists():
        return ""

    words = set(
        re.findall(r"[a-zA-Z]{3,}", query.lower())
    )

    if not words:
        return ""

    results = []

    for file in KNOWLEDGE_DIR.glob("*.md"):
        content = file.read_text(encoding="utf-8")

        # Split the document into sections
        sections = re.split(r"(?=^###? )", content, flags=re.M)

        for section in sections:
            section_words = set(
                re.findall(r"[a-zA-Z]{3,}", section.lower())
            )

            score = len(words & section_words)

            if score > 0:
                results.append((score, file.name, section))

    results.sort(key=lambda item: item[0], reverse=True)

    selected = results[:max_results]

    if not selected:
        return ""

    return "\n\n".join(
        f"Source: {filename}\n{section[:2500]}"
        for _, filename, section in selected
    )
