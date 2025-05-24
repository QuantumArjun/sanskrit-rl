import pytest, textwrap
from src.verifier import verify_meter

GOOD_ANUSHTUPH = textwrap.dedent("""
    धर्मो रक्षति रक्षितः
    धर्मो हन्ति निहन्यते
    """)  # quick fake example; should scan as Anuṣṭubh

BAD_ANUSHTUPH = "गा गा गा\nगा"

def test_passes_correct_meter():
    assert verify_meter(GOOD_ANUSHTUPH, "Anuṣṭup (Śloka)")

def test_fails_wrong_meter():
    assert not verify_meter(BAD_ANUSHTUPH, "Anuṣṭup (Śloka)")
