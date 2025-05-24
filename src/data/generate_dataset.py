"""
Produces prompts.jsonl in repo root.

Each line: {"topic": "...", "meter": "..."}
"""
from __future__ import annotations
import json, itertools, random
from pathlib import Path

TOPICS = [
    # Traditional Rasas (Emotional Essences) and their manifestations
    "शृङ्गारः (romantic love)", "विप्रलम्भः (love in separation)", "सम्भोगः (love in union)",
    "वीररसः (heroism)", "युद्धवीरः (battle heroism)", "दानवीरः (heroic generosity)", "धर्मवीरः (moral heroism)",
    "करुणा (pathos)", "शोकः (grief)", "वियोगः (separation)", "दुःखम् (sorrow)",
    "अद्भुतम् (wonder)", "विस्मयः (amazement)", "आश्चर्यम् (astonishment)",
    "हास्यम् (humor)", "विदूषकः (jester)", "परिहासः (jest)",
    "भयानकम् (terror)", "भयम् (fear)", "त्रासः (dread)",
    "रौद्रम् (fury)", "क्रोधः (anger)", "कोपः (wrath)",
    "शान्तम् (peace)", "निर्वाणम् (nirvana)", "शमः (tranquility)",
    
    # Seasons and their aspects
    "वसन्तः (spring)", "मधुमासः (honey month)", "कुसुमसमयः (flowering time)",
    "ग्रीष्मः (summer)", "आतपः (intense heat)", "सूर्यतापः (sun’s heat)",
    "वर्षा (monsoon)", "मेघागमः (cloud arrival)", "धारावर्षम् (downpour)",
    "शरत् (autumn)", "काशपुष्पम् (kash flowers)", "निर्मलाकाशः (clear sky)",
    "हेमन्तः (early winter)", "शीतकालः (cold season)", "तुषारः (frost)",
    "शिशिरः (late winter)", "हिमपातः (snowfall)", "शीतलवायुः (cold wind)",
    
    # Natural Elements and their forms
    "सागरः (ocean)", "तरङ्गाः (waves)", "महोदधिः (great ocean)", "जलधिः (sea)",
    "पर्वताः (mountains)", "हिमालयः (Himalayas)", "गिरिशृङ्गम् (peak)", "शैलः (rock mountain)",
    "वनम् (forest)", "अरण्यम् (wilderness)", "काननम् (grove)", "निकुञ्जः (bower)",
    "नद्यः (rivers)", "गङ्गा (Ganges)", "यमुना (Yamuna)", "सरस्वती (Saraswati)",
    "आकाशः (sky)", "मेघाः (clouds)", "नक्षत्राणि (stars)", "सूर्यः (sun)",
    "पृथिवी (earth)", "भूमिः (ground)", "धरा (world)", "वसुधा (earth goddess)",
    
    # Flora and Fauna
    "पद्मम् (lotus)", "कमलम् (lotus)", "पङ्कजम् (mud-born)",
    "मालती (jasmine)", "चम्पकः (champak)", "केतकी (screwpine)",
    "हंसः (swan)", "मयूरः (peacock)", "कोकिलः (cuckoo)",
    "सिंहः (lion)", "गजः (elephant)", "व्याघ्रः (tiger)",
    
    # Celestial Beings
    "देवाः (gods)", "इन्द्रः (Indra)", "विष्णुः (Vishnu)", "शिवः (Shiva)",
    "गन्धर्वाः (celestial musicians)", "किन्नराः (celestial beings)", "अप्सरसः (celestial nymphs)",
    "ब्रह्मा (Brahma)", "सरस्वती (Saraswati)", "लक्ष्मीः (Lakshmi)",
    
    # Philosophical Concepts
    "ज्ञानयोगः (path of knowledge)", "विद्या (learning)", "बोधः (understanding)",
    "भक्तिः (devotion)", "श्रद्धा (faith)", "उपासना (worship)",
    "ध्यानम् (meditation)", "समाधिः (concentration)", "योगः (yoga)",
    "मोक्षः (liberation)", "मुक्तिः (freedom)", "कैवल्यम् (absolute freedom)",
    "धर्मः (righteousness)", "न्यायः (justice)", "सत्यम् (truth)",
    "कर्मयोगः (path of action)", "सेवा (service)", "कर्तव्यम् (duty)",
    
    # Epic and Heroic Themes
    "युद्धम् (battle)", "संग्रामः (warfare)", "रणम् (combat)",
    "शौर्यम् (heroism)", "पराक्रमः (valor)", "वीर्यम् (prowess)",
    "त्यागः (sacrifice)", "बलिदानम् (offering)", "आत्मार्पणम् (self-sacrifice)",
    "विजयः (victory)", "जयः (triumph)", "सफलता (success)",
    
    # Cultural and Social Elements
    "गुरुपूजा (guru-worship)", "शिष्यत्वम् (discipleship)", "विद्यार्थी (student)",
    "उत्सवः (festival)", "समारोहः (celebration)", "महोत्सवः (grand festival)",
    "विवाहः (wedding)", "पाणिग्रहणम् (marriage)", "कल्याणम् (auspicious union)",
    "राजसभा (royal court)", "दरबारः (court)", "राज्यसभा (state assembly)",
    "मैत्री (friendship)", "सख्यम् (companionship)", "सौहार्दम् (amity)",
    
    # Abstract Concepts and Virtues
    "कालः (time)", "समयः (period)", "युगम् (epoch)",
    "सत्यम् (truth)", "धर्मः (duty)", "न्यायः (justice)",
    "कीर्तिः (fame)", "यशः (glory)", "प्रतिष्ठा (renown)",
    "आनन्दः (bliss)", "सुखम् (happiness)", "हर्षः (joy)",
    "क्षमा (forgiveness)", "दया (compassion)", "कृपा (mercy)"
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