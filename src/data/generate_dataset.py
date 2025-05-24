"""
Produces prompts.jsonl in repo root.

Each line: {"topic": "...", "meter": "..."}
"""
from __future__ import annotations
import json, itertools, random
from pathlib import Path

TOPICS = [
    # Traditional Rasas (Emotional Essences)
    "शृङ्गारः (love)", "वीररसः (valor)", "करुणा (pathos)", "अद्भुतम् (wonder)",
    "हास्यम् (humor)", "भयानकम् (terror)", "रौद्रम् (fury)", "शान्तम् (peace)",
    
    # Natural Elements and Seasons
    "वसन्तः (spring)", "वर्षा (monsoon)", "शरत् (autumn)", "हेमन्तः (winter)",
    "सागरः (ocean)", "पर्वताः (mountains)", "वनम् (forest)", "नद्यः (rivers)",
    
    # Philosophical and Spiritual
    "ज्ञानयोगः (path of knowledge)", "भक्तिः (devotion)", "ध्यानम् (meditation)",
    "मोक्षः (liberation)", "धर्मः (righteousness)", "कर्मयोगः (path of action)",
    
    # Heroic and Epic
    "युद्धम् (battle)", "शौर्यम् (heroism)", "त्यागः (sacrifice)", "विजयः (victory)",
    
    # Cultural and Social
    "गुरुपूजा (guru-worship)", "उत्सवः (festival)", "विवाहः (wedding)",
    "राजसभा (royal court)", "मैत्री (friendship)", "प्रेम (love)",
    
    # Abstract Concepts
    "कालः (time)", "सत्यम् (truth)", "कीर्तिः (fame)", "आनन्दः (bliss)",
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