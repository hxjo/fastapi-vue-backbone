import re


def has_password_various_chars(password: str) -> bool:
    # Check for at least 1 uppercase, 1 lowercase, 1 number, and 1 special character
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True


def is_strong_password(
    password: str,
) -> bool:
    """Check if a password is strong."""

    # Check the length
    if len(password) < 8:
        return False

    # Check against common passwords
    if password in common_passwords:
        return False

    if not has_password_various_chars(password):
        return False

    return True


common_passwords = [
    "password",
    "123456789",
    "12345678",
    "12345",
    "1234567",
    "sunshine",
    "qwerty",
    "iloveyou",
    "princess",
    "admin",
    "welcome",
    "666666",
    "abc123",
    "football",
    "123123",
    "monkey",
    "654321",
    "superman",
    "1qaz2wsx",
    "7777777",
    "121212",
    "000000",
    "qazwsx",
    "123qwe",
    "killer",
    "trustno1",
    "jordan",
    "jennifer",
    "zxcvbnm",
    "asdfgh",
    "hunter",
    "buster",
    "soccer",
    "harley",
    "batman",
    "andrew",
    "tigger",
    "2000",
    "charlie",
    "robert",
    "thomas",
    "hockey",
    "ranger",
    "daniel",
    "starwars",
    "klaster",
    "admin123",
]
