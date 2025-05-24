from __future__ import annotations
from typing import Literal
import chandas
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

Script = Literal["devanagari", "iast", "slp1", "hk"]

def _to_devanagari(text: str, script: Script) -> str:
    """Ensure Devanāgarī input for Chandas."""
    if script == "devanagari":
        return text
    mapping = {
        "iast": sanscript.IAST,
        "slp1": sanscript.SLP1,
        "hk": sanscript.HK,
    }[script]
    return transliterate(text, mapping, sanscript.DEVANAGARI)

def verify_meter(poem: str, expected_meter: str, script: Script = "devanagari", strict_match: bool = True) -> bool:
    """
    Returns True iff `poem` is scanned by Chandas as `expected_meter`.
    """
    poem_deva = _to_devanagari(poem, script)
    lines = [ln.strip() for ln in poem_deva.splitlines() if ln.strip()]
    patterns = chandas.to_pattern_lines(lines)
    result = chandas.svat_identifier.IdentifyFromPatternLines(patterns)
    
    # Get the actual values, and check for exact or accidental
    exact = list(result.get("exact", []))
    accidental = list(result.get("accidental", []))

    return expected_meter in exact if strict_match else expected_meter in exact + accidental
