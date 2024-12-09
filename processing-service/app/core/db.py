import logging

from sqlmodel import Session, create_engine

from app.core.config import settings
from app.models import Event, UserQuestReward # If deleted the tables won't be created

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    
