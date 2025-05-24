"""
Reward calculation for Sanskrit meter verification.
Uses the existing verifier to determine if the generated text matches the target meter.
"""

from typing import Dict
from .verifier import verify_meter

def calculate_reward(text: str, target_meter: str) -> Dict[str, float]:
    """
    Calculate reward for generated Sanskrit text based on meter correctness.
    
    Args:
        text: The generated Sanskrit text to verify
        target_meter: The name of the target meter (e.g. "अनुष्टुप्", "मन्दाक्रान्ता")
    
    Returns:
        Dictionary containing:
        - reward: 1.0 for exact match, 0.5 for accidental match, 0.0 otherwise
    """
    # Check for exact match
    if verify_meter(text, target_meter, strict_match=True):
        return {"reward": 1.0}
    
    # Check for accidental match
    if verify_meter(text, target_meter, strict_match=False):
        return {"reward": 0.5}
    
    # No match
    return {"reward": 0.0}
