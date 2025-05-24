"""
Produces prompts.jsonl in repo root.

Each line: {"topic": "...", "meter": "..."}
"""
from __future__ import annotations
import json, itertools, random
from pathlib import Path

TOPICS = [
    "शौर्यम् (heroism)", "वसन्तः (spring)", "गुरुपूजा (guru‑worship)",
    "करुणा (compassion)", "सागरः (the ocean)", "निर्वाणम् (liberation)",
    "वीररसः (valour)", "प्रकृति: (nature)", "ज्ञानयोगः (path of knowledge)",
]

METERS = [
    "अनुष्टुप्", "मन्दाक्रान्ता", "शार्दूलविक्रीडितम्",
    "वसन्ततिलका", "प्रियदर्शिनी", "त्रिष्टुप्", "जगती",
]

def format_prompt(entry: dict) -> str:
    """Format a prompt entry into a complete instruction."""
    return f"""\
Please write a Sanskrit poem in {entry['meter']} meter on the theme of "{entry['topic']}".
Return only the poem in Devanagari script, without any explanation.
"""

def main() -> None:
    # Create all combinations of topics and meters
    base_entries = [{"topic": t, "meter": m}
                   for t, m in itertools.product(TOPICS, METERS)]
    random.shuffle(base_entries)
    
    # Add formatted prompts
    entries = [{
        **entry,
        "prompt": format_prompt(entry)
    } for entry in base_entries]

    out = Path(__file__).parent / "prompts.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✔  Wrote {len(entries)} prompts to {out}")

if __name__ == "__main__":
    main()