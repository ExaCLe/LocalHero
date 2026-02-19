"""Integration tests for authentication endpoints."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ["JWT_SECRET_KEY"] = "test_secret_key_for_testing"


@pytest.fixture
def db_session(database_url: str) -> Session:  # type: ignore
    """Get a database session for direct DB access in tests."""
    # Import engine after DATABASE_URL is set
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def clean_db(db_session: Session) -> None:
    """Clean up database before each test."""
    from app.models.users import LoginActivity, User

    db_session.query(LoginActivity).delete()
    db_session.query(User).delete()
    db_session.commit()


class TestRegistration:
    """Test user registration endpoint."""

    def test_register_valid_user(self, api_client: TestClient, clean_db: None) -> None:
        """Test registration with valid data."""
        response = api_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "Registration successful" in data["message"]
        assert "verify" in data["message"].lower()

    def test_register_duplicate_email(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with duplicate email."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser1",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
        }
        api_client.post("/auth/register", json=user_data)

        # Try to register with same email
        response = api_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser2",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 400
        assert "email" in response.json()["detail"]

    def test_register_duplicate_email_case_insensitive(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with duplicate email (case-insensitive)."""
        api_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser1",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        response = api_client.post(
            "/auth/register",
            json={
                "email": "TEST@EXAMPLE.COM",
                "username": "testuser2",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 400
        assert "email" in response.json()["detail"]

    def test_register_duplicate_username(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with duplicate username."""
        api_client.post(
            "/auth/register",
            json={
                "email": "test1@example.com",
                "username": "testuser",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        response = api_client.post(
            "/auth/register",
            json={
                "email": "test2@example.com",
                "username": "testuser",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 400
        assert "username" in response.json()["detail"]

    def test_register_duplicate_username_case_insensitive(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with duplicate username (case-insensitive)."""
        api_client.post(
            "/auth/register",
            json={
                "email": "test1@example.com",
                "username": "testuser",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        response = api_client.post(
            "/auth/register",
            json={
                "email": "test2@example.com",
                "username": "TESTUSER",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 400
        assert "username" in response.json()["detail"]

    def test_register_weak_password_too_short(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with password too short."""
        response = api_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "short",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 400
        assert "password" in response.json()["detail"]

    def test_register_weak_password_common(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with common password."""
        response = api_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password1",  # Common password in blocklist
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 400
        assert "password" in response.json()["detail"]

    def test_register_invalid_username_special_chars(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with invalid username (special characters)."""
        response = api_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "test@user!",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 422  # Pydantic validation error

    def test_register_invalid_username_too_short(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with username too short."""
        response = api_client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "username": "ab",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 422

    def test_register_invalid_email(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test registration with invalid email."""
        response = api_client.post(
            "/auth/register",
            json={
                "email": "invalid-email",
                "username": "testuser",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        assert response.status_code == 422


class TestLogin:
    """Test user login endpoint."""

    def _create_verified_user(
        self, api_client: TestClient, db_session: Session
    ) -> dict[str, str]:
        """Helper to create a verified user for login tests."""
        from app.crud import get_user_by_email

        user_data = {
            "email": "verified@example.com",
            "username": "verifieduser",
            "password": "SecurePass123!",
            "first_name": "Verified",
            "last_name": "User",
        }
        api_client.post("/auth/register", json=user_data)

        # Manually verify the user
        user = get_user_by_email(db_session, user_data["email"])
        if user:
            user.is_email_verified = True  # type: ignore[assignment]
            db_session.commit()

        return user_data

    def test_login_with_valid_email(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test login with valid email and password."""
        user_data = self._create_verified_user(api_client, db_session)

        response = api_client.post(
            "/auth/login",
            json={"email": user_data["email"], "password": user_data["password"]},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert "user" in data
        assert data["user"]["email"] == user_data["email"]

    def test_login_with_valid_username(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test login with valid username and password."""
        user_data = self._create_verified_user(api_client, db_session)

        response = api_client.post(
            "/auth/login",
            json={"email": user_data["username"], "password": user_data["password"]},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_with_wrong_password(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test login with wrong password returns generic error."""
        user_data = self._create_verified_user(api_client, db_session)

        response = api_client.post(
            "/auth/login",
            json={"email": user_data["email"], "password": "WrongPassword123!"},
        )

        assert response.status_code == 401
        assert "Invalid email/username or password" in response.json()["detail"]

    def test_login_with_nonexistent_user(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test login with non-existent user returns generic error."""
        response = api_client.post(
            "/auth/login",
            json={"email": "nonexistent@example.com", "password": "SomePassword123!"},
        )

        assert response.status_code == 401
        assert "Invalid email/username or password" in response.json()["detail"]

    def test_login_with_unverified_email(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test login with unverified email returns specific error."""
        # Register but don't verify
        api_client.post(
            "/auth/register",
            json={
                "email": "unverified@example.com",
                "username": "unverified",
                "password": "SecurePass123!",
                "first_name": "Unverified",
                "last_name": "User",
            },
        )

        response = api_client.post(
            "/auth/login",
            json={"email": "unverified@example.com", "password": "SecurePass123!"},
        )

        assert response.status_code == 403
        data = response.json()["detail"]
        assert "verify your email" in data["detail"]
        assert data["email_not_verified"] is True

    def test_login_case_insensitive_email(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test login is case-insensitive for email."""
        user_data = self._create_verified_user(api_client, db_session)

        response = api_client.post(
            "/auth/login",
            json={
                "email": user_data["email"].upper(),
                "password": user_data["password"],
            },
        )

        assert response.status_code == 200


class TestLoginActivity:
    """Test login activity logging."""

    def _create_verified_user(
        self, api_client: TestClient, db_session: Session
    ) -> dict[str, str]:
        """Helper to create a verified user."""
        from app.crud import get_user_by_email

        user_data = {
            "email": "activity@example.com",
            "username": "activityuser",
            "password": "SecurePass123!",
            "first_name": "Activity",
            "last_name": "User",
        }
        api_client.post("/auth/register", json=user_data)
        user = get_user_by_email(db_session, user_data["email"])
        if user:
            user.is_email_verified = True  # type: ignore[assignment]
            db_session.commit()
        return user_data

    def test_successful_login_logged(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test that successful login is logged."""
        from app.models.users import LoginActivity

        user_data = self._create_verified_user(api_client, db_session)

        api_client.post(
            "/auth/login",
            json={"email": user_data["email"], "password": user_data["password"]},
        )

        activities = (
            db_session.query(LoginActivity)
            .filter(LoginActivity.email_attempted == user_data["email"])
            .all()
        )
        assert len(activities) == 1
        assert activities[0].success is True
        assert activities[0].user_id is not None

    def test_failed_login_wrong_password_logged(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test that failed login with wrong password is logged."""
        from app.models.users import LoginActivity

        user_data = self._create_verified_user(api_client, db_session)

        api_client.post(
            "/auth/login",
            json={"email": user_data["email"], "password": "WrongPassword123!"},
        )

        activities = (
            db_session.query(LoginActivity)
            .filter(LoginActivity.email_attempted == user_data["email"])
            .all()
        )
        assert len(activities) == 1
        assert activities[0].success is False
        assert activities[0].failure_reason == "invalid_password"

    def test_failed_login_nonexistent_user_logged(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test that failed login with non-existent user is logged."""
        from app.models.users import LoginActivity

        api_client.post(
            "/auth/login",
            json={"email": "nobody@example.com", "password": "SomePassword123!"},
        )

        activities = (
            db_session.query(LoginActivity)
            .filter(LoginActivity.email_attempted == "nobody@example.com")
            .all()
        )
        assert len(activities) == 1
        assert activities[0].success is False
        assert activities[0].failure_reason == "user_not_found"
        assert activities[0].user_id is None


class TestProtectedEndpoints:
    """Test protected endpoint access."""

    def _create_verified_user_and_token(
        self, api_client: TestClient, db_session: Session
    ) -> tuple[dict[str, str], str]:
        """Helper to create a verified user and get token."""
        from app.crud import get_user_by_email

        user_data = {
            "email": "protected@example.com",
            "username": "protecteduser",
            "password": "SecurePass123!",
            "first_name": "Protected",
            "last_name": "User",
        }
        api_client.post("/auth/register", json=user_data)
        user = get_user_by_email(db_session, user_data["email"])
        if user:
            user.is_email_verified = True  # type: ignore[assignment]
            db_session.commit()

        login_response = api_client.post(
            "/auth/login",
            json={"email": user_data["email"], "password": user_data["password"]},
        )
        token = login_response.json()["access_token"]
        return user_data, token

    def test_logout_with_valid_token(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test logout with valid token."""
        _, token = self._create_verified_user_and_token(api_client, db_session)

        response = api_client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert "logged out" in response.json()["message"]

    def test_logout_without_token(self, api_client: TestClient, clean_db: None) -> None:
        """Test logout without token."""
        response = api_client.post("/auth/logout")

        assert response.status_code == 401

    def test_logout_with_invalid_token(
        self, api_client: TestClient, clean_db: None
    ) -> None:
        """Test logout with invalid token."""
        response = api_client.post(
            "/auth/logout",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401

    def test_logout_with_expired_token(
        self, api_client: TestClient, db_session: Session, clean_db: None
    ) -> None:
        """Test logout with expired token."""
        from datetime import timedelta

        from app.crud import get_user_by_email
        from app.security.jwt import create_access_token

        # Create user first
        user_data = {
            "email": "expired@example.com",
            "username": "expireduser",
            "password": "SecurePass123!",
            "first_name": "Expired",
            "last_name": "User",
        }
        api_client.post("/auth/register", json=user_data)
        user = get_user_by_email(db_session, user_data["email"])
        if user:
            user.is_email_verified = True  # type: ignore[assignment]
            db_session.commit()

            # Create expired token
            expired_token = create_access_token(user.id, expires_delta=timedelta(seconds=-1))  # type: ignore[arg-type]

            response = api_client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {expired_token}"},
            )

            assert response.status_code == 401
