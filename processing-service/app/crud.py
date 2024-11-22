from typing import Any
import uuid

from sqlmodel import Session, select

from app.models import Event, EventCreate, UserQuestReward, UserQuestRewardCreate, UserQuestRewardUpdate

def create_user_quest_reward(*, session: Session, user_quest_reward_create: UserQuestRewardCreate) -> UserQuestReward:
    db_user_quest_reward = UserQuestReward.model_validate(user_quest_reward_create)
    session.add(db_user_quest_reward)
    session.commit()
    session.refresh(db_user_quest_reward)
    return db_user_quest_reward

def update_user_quest_reward(*, session: Session, db_user_quest_reward: UserQuestReward, user_quest_reward_update: UserQuestRewardUpdate) -> Any:
    user_quest_reward_data = user_quest_reward_update.model_dump(exclude_unset=True)
    db_user_quest_reward.sqlmodel_update(user_quest_reward_data)
    session.add(db_user_quest_reward)
    session.commit()
    session.refresh(db_user_quest_reward)
    return db_user_quest_reward

def get_user_quest_reward_by_user_id_quest_id(*, session: Session, user_id: uuid.UUID, quest_id: uuid.UUID) -> UserQuestReward | None:
    statement = select(UserQuestReward).where((UserQuestReward.user_id == user_id) & (UserQuestReward.quest_id == quest_id))
    session_user = session.exec(statement).first()
    return session_user

def create_event(*, session: Session, event_create: EventCreate) -> Event:
    db_event = Event.model_validate(event_create)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event