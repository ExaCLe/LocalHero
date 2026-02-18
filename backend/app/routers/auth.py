from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
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
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _get_user_agent(request: Request) -> str:
    return request.headers.get("User-Agent", "unknown")


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:
    errors: dict[str, list[str]] = {}

    if get_user_by_email(db, user_data.email):
        errors["email"] = ["A user with this email already exists"]

    if get_user_by_username(db, user_data.username):
        errors["username"] = ["A user with this username already exists"]

    password_errors = validate_password_strength(user_data.password)
    if password_errors:
        errors["password"] = password_errors

    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errors,
        )

    try:
        create_user(db, user_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"email": ["A user with this email or username already exists"]},
        )

    return RegisterResponse(
        message="Registration successful. Please check your email to verify your account."
    )


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UserLogin, request: Request, db: Session = Depends(get_db)
) -> TokenResponse:
    ip_address = _get_client_ip(request)
    user_agent = _get_user_agent(request)
    generic_error = "Invalid email/username or password"

    user = get_user_by_email_or_username(db, login_data.email)

    if user is None:
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

    if not verify_password(login_data.password, cast(str, user.password_hash)):
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

    if not user.is_email_verified:
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
            detail={
                "detail": "Please verify your email before logging in",
                "email_not_verified": True,
            },
        )

    create_login_activity(
        db=db,
        email_attempted=login_data.email,
        ip_address=ip_address,
        user_agent=user_agent,
        success=True,
        user_id=cast(int, user.id),
    )

    access_token = create_access_token(cast(int, user.id))

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserRead.model_validate(user),
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(_: User = Depends(get_current_user)) -> LogoutResponse:
    return LogoutResponse(message="Successfully logged out")
