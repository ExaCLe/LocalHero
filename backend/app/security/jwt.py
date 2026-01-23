import os
from datetime import UTC, datetime, timedelta
from typing import cast

import jwt  # type: ignore[import-not-found]
from pydantic import BaseModel

# JWT configuration from environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class TokenPayload(BaseModel):
    """Token payload schema."""

    sub: str
    exp: datetime
    iat: datetime
    type: str


def _get_secret_key() -> str:
    """Get the JWT secret key, raising an error if not set."""
    if not JWT_SECRET_KEY:
        raise RuntimeError(
            "JWT_SECRET_KEY environment variable is required but not set"
        )
    return JWT_SECRET_KEY


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token for the given user_id.

    Args:
        user_id: The user's ID to encode in the token
        expires_delta: Optional custom expiration time delta

    Returns:
        Encoded JWT token string
    """
    secret_key = _get_secret_key()

    now = datetime.now(UTC)
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = now + expires_delta

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": now,
        "type": "access",
    }

    return cast(str, jwt.encode(payload, secret_key, algorithm=JWT_ALGORITHM))


def decode_access_token(token: str) -> TokenPayload | None:
    """
    Decode and validate a JWT access token.

    Args:
        token: The JWT token string to decode

    Returns:
        TokenPayload if valid, None if invalid or expired
    """
    try:
        secret_key = _get_secret_key()
        payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])

        # Verify token type
        if payload.get("type") != "access":
            return None

        return TokenPayload(
            sub=payload["sub"],
            exp=datetime.fromtimestamp(payload["exp"], tz=UTC),
            iat=datetime.fromtimestamp(payload["iat"], tz=UTC),
            type=payload["type"],
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except (KeyError, ValueError):
        return None
