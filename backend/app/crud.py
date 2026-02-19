from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.users import LoginActivity, User
from app.schemas.auth import UserCreate
from app.security.password import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(func.lower(User.email) == email.lower()).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(func.lower(User.username) == username.lower()).first()


def get_user_by_email_or_username(db: Session, identifier: str) -> User | None:
    return (
        db.query(User)
        .filter(
            (func.lower(User.email) == identifier.lower())
            | (func.lower(User.username) == identifier.lower())
        )
        .first()
    )


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        email=user_data.email.lower(),
        username=user_data.username.lower(),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password_hash=hash_password(user_data.password),
        is_email_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_login_activity(
    db: Session,
    email_attempted: str,
    ip_address: str,
    user_agent: str,
    success: bool,
    user_id: int | None = None,
    failure_reason: str | None = None,
) -> LoginActivity:
    activity = LoginActivity(
        user_id=user_id,
        email_attempted=email_attempted,
        ip_address=ip_address,
        user_agent=user_agent,
        success=success,
        failure_reason=failure_reason,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity
