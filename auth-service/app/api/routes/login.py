from datetime import timedelta, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.core import security
from app.core.config import settings
from app.core.events import publish_event
from app.models import  Token, UserPublic, UserUpdate, Event

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, user_name=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect user_name or password")
    elif user.status == 2:
        raise HTTPException(status_code=400, detail="Banned user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if user.status == 1:
        event_in = Event(event_type="UserSignIn", user_id=user.user_id, timestamp=datetime.now())
        publish_event(event_in)

    if user.status == 0:
        event_in = Event(event_type="NewUserSignIn", user_id=user.user_id, timestamp=datetime.now())
        publish_event(event_in)
        user_in = UserUpdate(status=1)
        crud.update_user(session=session, db_user=user, user_in=user_in)
    
    return Token(
        access_token=security.create_access_token(
            user.user_id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
