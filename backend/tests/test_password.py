"""Tests for password hashing and validation."""

import pytest

from app.security.password import hash_password, validate_password_strength, verify_password


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_hash_password_returns_string(self) -> None:
        """Test that hash_password returns a string."""
        result = hash_password("test_password_123")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_hash_password_different_for_same_input(self) -> None:
        """Test that hash_password returns different hashes for same password (salt)."""
        hash1 = hash_password("test_password_123")
        hash2 = hash_password("test_password_123")
        assert hash1 != hash2

    def test_verify_password_correct(self) -> None:
        """Test that verify_password returns True for correct password."""
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self) -> None:
        """Test that verify_password returns False for incorrect password."""
        hashed = hash_password("test_password_123")
        assert verify_password("wrong_password", hashed) is False


class TestPasswordStrengthValidation:
    """Test password strength validation."""

    def test_valid_password_returns_empty_list(self) -> None:
        """Test that a valid password returns no errors."""
        result = validate_password_strength("ValidPass123")
        assert result == []

    def test_password_too_short(self) -> None:
        """Test that password under 10 characters returns error."""
        result = validate_password_strength("short123")
        assert any("at least 10 characters" in error for error in result)

    def test_password_minimum_length(self) -> None:
        """Test that password exactly 10 characters is valid."""
        result = validate_password_strength("exactly10c")
        length_errors = [e for e in result if "10 characters" in e]
        assert len(length_errors) == 0

    def test_password_too_long(self) -> None:
        """Test that password over 64 characters returns error."""
        long_password = "a" * 65
        result = validate_password_strength(long_password)
        assert any("at most 64 characters" in error for error in result)

    def test_password_maximum_length(self) -> None:
        """Test that password exactly 64 characters is valid."""
        max_password = "a" * 64
        result = validate_password_strength(max_password)
        length_errors = [e for e in result if "64 characters" in e]
        assert len(length_errors) == 0

    def test_common_password_rejected(self) -> None:
        """Test that common passwords are rejected."""
        # "password1" should be in the blocklist
        result = validate_password_strength("password1")
        assert any("too common" in error for error in result)

    def test_common_password_case_insensitive(self) -> None:
        """Test that common password check is case-insensitive."""
        result = validate_password_strength("PASSWORD1")
        assert any("too common" in error for error in result)

    def test_multiple_errors_returned(self) -> None:
        """Test that multiple validation errors can be returned."""
        # Short and common password
        result = validate_password_strength("password")
        assert len(result) >= 2  # At least length and blocklist errors
