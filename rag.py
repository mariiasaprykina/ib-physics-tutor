
from pathlib import Path
from collections import Counter
import json
import math
import re

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"
INDEX_PATH = KNOWLEDGE_DIR / "openstax_index.json"

# Common English words that are not useful for searching
STOP_WORDS = {
    "the", "and", "for", "with", "from", "this", "that",
    "what", "when", "where", "which", "about", "into",
    "have", "does", "how", "why", "can", "you", "are",
    "please", "help", "solve", "problem", "question",
    "physics", "explain", "using"
}


def tokenize(text):
    """Extract meaningful English search terms."""
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def retrieve_knowledge(query, max_results=3):
    """Search OpenStax index and local Markdown materials."""

    if not KNOWLEDGE_DIR.exists():
        return ""

    query_words = set(tokenize(query))

    if not query_words:
        return ""

    documents = []

    # 1. Load indexed OpenStax textbook
    if INDEX_PATH.exists():
        try:
            with INDEX_PATH.open("r", encoding="utf-8") as file:
                chunks = json.load(file)

            for chunk in chunks:
                documents.append({
                    "text": chunk.get("text", ""),
                    "source": chunk.get("source", "OpenStax Physics"),
                    "page": chunk.get("pdf_page"),
                    "url": chunk.get("source_url", "")
                })

        except (OSError, json.JSONDecodeError) as error:
            print(f"Could not load OpenStax index: {error}")

    # 2. Keep support for existing Markdown files
    for file in KNOWLEDGE_DIR.glob("*.md"):
        content = file.read_text(encoding="utf-8")

        sections = re.split(
            r"(?=^###? )",
            content,
            flags=re.MULTILINE
        )

        for section in sections:
            if section.strip():
                documents.append({
                    "text": section,
                    "source": file.name,
                    "page": None,
                    "url": ""
                })

    if not documents:
        return ""

    # 3. Calculate document frequency
    document_frequency = Counter()

    for document in documents:
        document["tokens"] = set(tokenize(document["text"]))
        document_frequency.update(document["tokens"])

    total_documents = len(documents)
    results = []

    # 4. Rank matching fragments using weighted keywords
    for document in documents:
        matching_words = query_words & document["tokens"]

        if not matching_words:
            continue

        score = sum(
            math.log(
                (total_documents + 1) /
                (document_frequency[word] + 1)
            ) + 1
            for word in matching_words
        )

        results.append((score, document))

    results.sort(key=lambda item: item[0], reverse=True)
    selected = results[:max_results]

    if not selected:
        return ""

    # 5. Return relevant material with source information
    passages = []

    for _, document in selected:
        source = document["source"]

        if document["page"] is not None:
            source += f", PDF page {document['page']}"

        if document["url"]:
            source += f"\nBook URL: {document['url']}"

        passages.append(
            f"Source: {source}\n"
            f"Reference text:\n{document['text'][:2200]}"
        )

    return "\n\n---\n\n".join(passages)
