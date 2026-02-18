from pathlib import Path
from typing import Any, cast

from pwdlib import PasswordHash  # type: ignore[import-not-found]
from pwdlib.hashers.argon2 import Argon2Hasher  # type: ignore[import-not-found]

_password_hash: Any = PasswordHash((Argon2Hasher(),))

_blocklist: set[str] = set()
_blocklist_path = Path(__file__).parent / "data" / "common_passwords.txt"
if _blocklist_path.exists():
    with _blocklist_path.open("r", encoding="utf-8") as f:
        _blocklist = {line.strip().lower() for line in f if line.strip()}


def hash_password(plain: str) -> str:
    return cast(str, _password_hash.hash(plain))


def verify_password(plain: str, hashed: str) -> bool:
    return cast(bool, _password_hash.verify(plain, hashed))


def validate_password_strength(password: str) -> list[str]:
    errors: list[str] = []

    if len(password) < 10:
        errors.append("Password must be at least 10 characters long")

    if len(password) > 64:
        errors.append("Password must be at most 64 characters long")

    if password.lower() in _blocklist:
        errors.append("Password is too common. Please choose a more unique password")

    return errors
