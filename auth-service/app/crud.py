
from typing import Any
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, EventClaim, EventClaimCreate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_username(*, session: Session, user_name: str) -> User | None:
    statement = select(User).where(User.user_name == user_name)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, user_name: str, password: str) -> User | None:
    db_user = get_user_by_username(session=session, user_name=user_name)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_event_claim(*, session: Session, event_claim_create: EventClaimCreate) -> EventClaim:
    db_obj = EventClaim.model_validate(event_claim_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj