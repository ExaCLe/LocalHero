import logging
import os
from datetime import UTC, datetime, timedelta
from typing import cast

import jwt  # type: ignore[import-not-found]
from pydantic import BaseModel

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
_DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES", str(_DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )
except ValueError:
    logging.warning(
        "Invalid ACCESS_TOKEN_EXPIRE_MINUTES value %r; falling back to default %d",
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
        _DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    ACCESS_TOKEN_EXPIRE_MINUTES = _DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    iat: datetime
    type: str


def _get_secret_key() -> str:
    if not JWT_SECRET_KEY:
        raise RuntimeError(
            "JWT_SECRET_KEY environment variable is required but not set"
        )
    return JWT_SECRET_KEY


def validate_jwt_config() -> None:
    """Validate JWT configuration at startup. Raises RuntimeError if invalid."""
    if not JWT_SECRET_KEY:
        raise RuntimeError(
            "JWT_SECRET_KEY environment variable is required but not set"
        )


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
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
    try:
        secret_key = _get_secret_key()
        payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])

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
