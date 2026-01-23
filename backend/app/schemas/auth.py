import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    username: str = Field(min_length=3, max_length=30)
    password: str
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Username must be alphanumeric + underscore only."""
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v


class UserRead(BaseModel):
    """Schema for reading user data (excludes password_hash)."""

    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_email_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """Schema for user login."""

    email: str = Field(description="Email address or username")
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserRead
