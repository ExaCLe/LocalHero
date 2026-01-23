"""Tests for JWT token handling."""

import os
from datetime import timedelta

import pytest

# Set JWT_SECRET_KEY before importing jwt module
os.environ["JWT_SECRET_KEY"] = "test_secret_key_for_testing"

from app.security.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    decode_access_token,
)


class TestJWTTokenCreation:
    """Test JWT token creation."""

    def test_create_access_token_returns_string(self) -> None:
        """Test that create_access_token returns a string."""
        token = create_access_token(user_id=1)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_custom_expiry(self) -> None:
        """Test that create_access_token accepts custom expiry."""
        token = create_access_token(user_id=1, expires_delta=timedelta(hours=1))
        assert isinstance(token, str)


class TestJWTTokenDecoding:
    """Test JWT token decoding."""

    def test_decode_valid_token(self) -> None:
        """Test decoding a valid token."""
        token = create_access_token(user_id=123)
        payload = decode_access_token(token)

        assert payload is not None
        assert payload.sub == "123"
        assert payload.type == "access"

    def test_decode_invalid_token(self) -> None:
        """Test that invalid token returns None."""
        result = decode_access_token("invalid_token")
        assert result is None

    def test_decode_tampered_token(self) -> None:
        """Test that tampered token returns None."""
        token = create_access_token(user_id=1)
        tampered = token[:-5] + "xxxxx"
        result = decode_access_token(tampered)
        assert result is None

    def test_decode_expired_token(self) -> None:
        """Test that expired token returns None."""
        token = create_access_token(user_id=1, expires_delta=timedelta(seconds=-1))
        result = decode_access_token(token)
        assert result is None

    def test_token_contains_correct_user_id(self) -> None:
        """Test that token contains the correct user_id."""
        user_id = 42
        token = create_access_token(user_id=user_id)
        payload = decode_access_token(token)

        assert payload is not None
        assert payload.sub == str(user_id)


class TestJWTConfiguration:
    """Test JWT configuration."""

    def test_default_expiry_minutes(self) -> None:
        """Test that default expiry is set."""
        assert ACCESS_TOKEN_EXPIRE_MINUTES > 0
