import logging

from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.user_name == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        logger.info(f'Superuser: {settings.FIRST_SUPERUSER} Password: {settings.FIRST_SUPERUSER_PASSWORD}')
        user_in = UserCreate(
            user_name=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.create_user(session=session, user_create=user_in)
