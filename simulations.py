import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent / 'knowledge' / 'simulations.json'

def recommend_simulations(topic=None, query='', level='SL', limit=3):
    """Return catalog entries only; no generated URLs."""
    entries = json.loads(CATALOG.read_text(encoding='utf-8'))
    words = set(re.findall(r'[^\W_]+', query.casefold()))
    topic = (topic or '').strip().upper()
    ranked = []
    for entry in entries:
        if level not in entry['levels']:
            continue
        match = topic == entry['topic']
        overlap = len(words.intersection(entry['keywords']))
        if topic and not match:
            continue
        score = 10 * match + overlap
        if score:
            ranked.append((score, entry))
    ranked.sort(key=lambda pair: -pair[0])
    return [entry for _, entry in ranked[:limit]]
