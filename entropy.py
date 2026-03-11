"""
entropy.py
----------
SecureVault – Advanced Password Generator and Manager
SynthBay Solutions | Founder: Harshvardhan Wadekar

Calculates password entropy (in bits) and determines password strength.
Entropy is a measure of unpredictability – higher entropy = harder to crack.
"""

import math
import string


def calculate_entropy(password: str) -> float:
    """
    Calculate Shannon entropy of a password in bits.

    Entropy formula: H = L × log2(N)
    Where:
        L = password length
        N = size of possible character pool (derived from character types used)

    Args:
        password (str): The password to evaluate.

    Returns:
        float: Entropy value in bits.
    """
    if not password:
        return 0.0

    # Determine which character categories are present in the password
    pool_size = 0

    has_lowercase = any(c in string.ascii_lowercase for c in password)
    has_uppercase = any(c in string.ascii_uppercase for c in password)
    has_digits    = any(c in string.digits for c in password)
    has_symbols   = any(c in string.punctuation for c in password)

    # Add the size of each detected character category to pool
    if has_lowercase:
        pool_size += 26   # a–z
    if has_uppercase:
        pool_size += 26   # A–Z
    if has_digits:
        pool_size += 10   # 0–9
    if has_symbols:
        pool_size += 32   # common special characters

    if pool_size == 0:
        return 0.0

    # H = length × log2(pool_size)
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)


def get_strength_label(entropy: float) -> str:
    """
    Classify password strength based on entropy value.

    Thresholds (in bits):
        < 40  → Weak
        40–59 → Medium
        60–79 → Strong
        ≥ 80  → Very Strong

    Args:
        entropy (float): Entropy value in bits.

    Returns:
        str: Strength label.
    """
    if entropy < 40:
        return "Weak"
    elif entropy < 60:
        return "Medium"
    elif entropy < 80:
        return "Strong"
    else:
        return "Very Strong"


def get_crack_time_estimate(entropy: float) -> str:
    """
    Estimate cracking resistance based on entropy bits.

    Assumes an attacker using offline cracking at ~10 billion guesses/sec
    (modern GPU cluster benchmark).

    Args:
        entropy (float): Entropy value in bits.

    Returns:
        str: Human-readable estimated cracking time.
    """
    if entropy <= 0:
        return "Instantly"

    # Number of possible combinations: 2^entropy
    combinations = 2 ** entropy

    # Attacker speed: 10 billion (1e10) guesses per second
    guesses_per_second = 1e10

    # Average time = half of total combinations / rate (in seconds)
    seconds = (combinations / 2) / guesses_per_second

    # Convert seconds into human-readable units
    if seconds < 1:
        return "Less than a second"
    elif seconds < 60:
        return f"{int(seconds)} second(s)"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minute(s)"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hour(s)"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} day(s)"
    elif seconds < 3.154e9:
        return f"{int(seconds / 31536000)} year(s)"
    elif seconds < 3.154e13:
        return f"{int(seconds / 3.154e9)} thousand year(s)"
    elif seconds < 3.154e16:
        return f"{int(seconds / 3.154e13)} million year(s)"
    else:
        return "Billions of years (uncrackable)"


def get_strength_color(label: str) -> str:
    """
    Return a hex color string corresponding to a strength label.
    Used for visual feedback in the GUI.

    Args:
        label (str): Strength label from get_strength_label().

    Returns:
        str: Hex color code.
    """
    colors = {
        "Weak":        "#FF4757",   # Red
        "Medium":      "#FFA502",   # Orange
        "Strong":      "#2ED573",   # Green
        "Very Strong": "#1E90FF",   # Blue
    }
    return colors.get(label, "#AAAAAA")
