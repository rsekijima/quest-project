import uuid

from sqlmodel import Session, select

from app.models import Reward, Quest, QuestCreate, RewardCreate


def create_reward(*, session: Session, reward_create: RewardCreate) -> Reward:
    db_reward = Reward.model_validate(reward_create)
    session.add(db_reward)
    session.commit()
    session.refresh(db_reward)
    return db_reward

def get_reward_by_name(*, session: Session, reward_name: str) -> Reward | None:
    statement = select(Reward).where(Reward.reward_name == reward_name)
    session_reward = session.exec(statement).first()
    return session_reward

def get_reward_by_id(*, session: Session, reward_id: int) -> Reward | None:
    statement = select(Reward).where(Reward.reward_id == reward_id)
    session_reward = session.exec(statement).first()
    return session_reward


def create_quest(*, session: Session, quest_in: QuestCreate, reward_id: uuid.UUID) -> Quest:
    db_quest = Quest.model_validate(quest_in, update={"reward_id": reward_id})
    session.add(db_quest)
    session.commit()
    session.refresh(db_quest)
    return db_quest


def get_quest_by_name(*, session: Session, name: str) -> Quest | None:
    statement = select(Quest).where(Quest.name == name)
    session_quest = session.exec(statement).first()
    return session_quest

def get_quest_by_id(*, session: Session, quest_id: int) -> Quest | None:
    statement = select(Quest).where(Quest.quest_id == quest_id)
    session_quest = session.exec(statement).first()
    return session_quest

