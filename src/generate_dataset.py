"""
Produces prompts.jsonl in repo root.

Each line: {"topic": "...", "meter": "..."}
"""
import json, itertools, random, pathlib

TOPICS = [
    "शौर्यम् (heroism)", "वसन्तः (spring)", "गुरुपूजा (guru‑worship)",
    "करुणा (compassion)", "सागरः (the ocean)", "निर्वाणम् (liberation)",
    "वीररसः (valour)", "प्रकृति: (nature)", "ज्ञानयोगः (path of knowledge)",
]

METERS = [
    "अनुष्टुप्", "मन्दाक्रान्ता", "शार्दूलविक्रीडितम्",
    "वसन्ततिलका", "प्रियदर्शिनी", "त्रिष्टुप्", "जगती",
]

def main() -> None:
    rows = [{"topic": t, "meter": m}
            for t, m in itertools.product(TOPICS, METERS)]
    random.shuffle(rows)

    out = Path(__file__).parent / "data" / "prompts.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✔  Wrote {len(rows)} prompts to {out}")

if __name__ == "__main__":
    main()