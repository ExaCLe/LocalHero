from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud import (
    create_login_activity,
    create_user,
    get_user_by_email,
    get_user_by_email_or_username,
    get_user_by_username,
)
from app.database import get_db
from app.dependencies import get_current_user
from app.models.users import User
from app.schemas.auth import TokenResponse, UserCreate, UserLogin, UserRead
from app.security.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.security.password import validate_password_strength, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterResponse(BaseModel):
    message: str


class LoginErrorResponse(BaseModel):
    detail: str
    email_not_verified: bool = False


class LogoutResponse(BaseModel):
    message: str


def _get_client_ip(request: Request) -> str:
    """Extract client IP address from request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _get_user_agent(request: Request) -> str:
    """Extract user agent from request."""
    return request.headers.get("User-Agent", "unknown")


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:
    """
    Register a new user.

    Validates:
    - Email format (via Pydantic EmailStr)
    - Email uniqueness (case-insensitive)
    - Username format (3-30 chars, alphanumeric + underscore) and uniqueness (case-insensitive)
    - Password strength (length + blocklist)
    """
    errors: dict[str, list[str]] = {}

    # Validate email uniqueness
    if get_user_by_email(db, user_data.email):
        errors["email"] = ["A user with this email already exists"]

    # Validate username uniqueness
    if get_user_by_username(db, user_data.username):
        errors["username"] = ["A user with this username already exists"]

    # Validate password strength
    password_errors = validate_password_strength(user_data.password)
    if password_errors:
        errors["password"] = password_errors

    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errors,
        )

    # Create user
    create_user(db, user_data)

    return RegisterResponse(message="Registration successful. Please check your email to verify your account.")


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Login a user.

    Flow:
    1. Find user by email or username (case-insensitive)
    2. If not found: log activity (failure, "user_not_found"), return generic error
    3. Verify password
    4. If wrong: log activity (failure, "invalid_password"), return generic error
    5. Check is_email_verified
    6. If not verified: log activity (failure, "email_not_verified"), return specific error
    7. Log activity (success)
    8. Generate access token
    9. Return TokenResponse
    """
    ip_address = _get_client_ip(request)
    user_agent = _get_user_agent(request)
    generic_error = "Invalid email/username or password"

    # Find user by email or username
    user = get_user_by_email_or_username(db, login_data.email)

    if user is None:
        # Log failed attempt - user not found
        create_login_activity(
            db=db,
            email_attempted=login_data.email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            failure_reason="user_not_found",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=generic_error,
        )

    # Verify password
    if not verify_password(login_data.password, cast(str, user.password_hash)):
        # Log failed attempt - invalid password
        create_login_activity(
            db=db,
            email_attempted=login_data.email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            user_id=cast(int, user.id),
            failure_reason="invalid_password",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=generic_error,
        )

    # Check email verification
    if not user.is_email_verified:
        # Log failed attempt - email not verified
        create_login_activity(
            db=db,
            email_attempted=login_data.email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=False,
            user_id=cast(int, user.id),
            failure_reason="email_not_verified",
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"detail": "Please verify your email before logging in", "email_not_verified": True},
        )

    # Log successful login
    create_login_activity(
        db=db,
        email_attempted=login_data.email,
        ip_address=ip_address,
        user_agent=user_agent,
        success=True,
        user_id=cast(int, user.id),
    )

    # Generate access token
    access_token = create_access_token(cast(int, user.id))

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserRead.model_validate(user),
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(_: User = Depends(get_current_user)) -> LogoutResponse:
    """
    Logout the current user.

    For now, this is a no-op on the backend (just returns success).
    Client is responsible for clearing the token.
    When refresh tokens are added (AL-9), this will revoke the token family.
    """
    return LogoutResponse(message="Successfully logged out")
