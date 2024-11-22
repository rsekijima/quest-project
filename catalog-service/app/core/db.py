import logging

from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import Reward, Quest, RewardCreate, QuestCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    reward = session.exec(
        select(Reward).where(Reward.reward_name == settings.FIRST_REWARD_NAME)
    ).first()
    if not reward:
        reward_in = RewardCreate(
            reward_name=settings.FIRST_REWARD_NAME,
            reward_item=settings.FIRST_REWARD_ITEM,
            reward_qty=settings.FIRST_REWARD_QUANTITY,
        )
        reward = crud.create_reward(session=session, reward_create=reward_in)
    
    quest = session.exec(
        select(Quest).where(Quest.name == settings.FIRST_QUEST_NAME)
    ).first()
    if not quest:
        quest_in = QuestCreate(
            name=settings.FIRST_QUEST_NAME,
            auto_claim=settings.FIRST_QUEST_AUTO_CLAIM,
            streak=settings.FIRST_QUEST_STEAK,
            duplication=settings.FIRST_QUEST_DUPLICATION,
        )
        quest = crud.create_quest(session=session, quest_in=quest_in, reward_id=reward.reward_id)
    
