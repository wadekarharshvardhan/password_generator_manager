"""
generator.py
------------
SecureVault – Advanced Password Generator and Manager
SynthBay Solutions | Founder: Harshvardhan Wadekar

Handles cryptographically secure password generation using Python's
secrets module, which is suitable for security-sensitive operations.
"""

import secrets
import string


# Character sets used for password generation
UPPERCASE = string.ascii_uppercase      # A-Z
LOWERCASE = string.ascii_lowercase      # a-z
DIGITS    = string.digits               # 0-9
SYMBOLS   = "!@#$%^&*()_+-=[]{}|;':\",./<>?"  # Special characters


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length (int): Desired password length (8–64).
        use_uppercase (bool): Include uppercase letters.
        use_lowercase (bool): Include lowercase letters.
        use_digits (bool): Include numeric digits.
        use_symbols (bool): Include special symbols.

    Returns:
        str: Generated password string.

    Raises:
        ValueError: If length is out of range or no character set selected.
    """
    if not (8 <= length <= 64):
        raise ValueError("Password length must be between 8 and 64 characters.")

    # Build the pool of characters from enabled categories
    character_pool = ""
    mandatory_chars = []  # Guarantee at least one char from each enabled set

    if use_uppercase:
        character_pool += UPPERCASE
        mandatory_chars.append(secrets.choice(UPPERCASE))

    if use_lowercase:
        character_pool += LOWERCASE
        mandatory_chars.append(secrets.choice(LOWERCASE))

    if use_digits:
        character_pool += DIGITS
        mandatory_chars.append(secrets.choice(DIGITS))

    if use_symbols:
        character_pool += SYMBOLS
        mandatory_chars.append(secrets.choice(SYMBOLS))

    if not character_pool:
        raise ValueError("At least one character type must be selected.")

    # Fill the remaining length with random choices from the full pool
    remaining_length = length - len(mandatory_chars)
    random_chars = [secrets.choice(character_pool) for _ in range(remaining_length)]

    # Combine mandatory + random characters, then shuffle securely
    all_chars = mandatory_chars + random_chars
    secrets.SystemRandom().shuffle(all_chars)  # Cryptographically secure shuffle

    return "".join(all_chars)
