
from pathlib import Path
import json
import re
import fitz

BASE = Path(__file__).resolve().parent
PDF_PATH = BASE / "openstax" / "physics.pdf"
OUTPUT_PATH = BASE / "openstax_index.json"

SOURCE_URL = "https://openstax.org/books/physics/pages/1-introduction"


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def build_index():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    chunks = []

    with fitz.open(PDF_PATH) as document:
        for page_number, page in enumerate(document, start=1):
            text = clean_text(page.get_text("text"))

            if not text:
                continue

            words = text.split()
            chunk_size = 220
            overlap = 40

            for start in range(0, len(words), chunk_size - overlap):
                part = words[start:start + chunk_size]

                if len(part) < 20:
                    continue

                chunks.append({
                    "source": "OpenStax Physics",
                    "source_url": SOURCE_URL,
                    "license": "CC BY 4.0",
                    "pdf_page": page_number,
                    "text": " ".join(part)
                })

    OUTPUT_PATH.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Indexed {len(chunks)} text chunks")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    build_index()
