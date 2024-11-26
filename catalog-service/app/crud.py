import uuid
import json
import logging

from sqlmodel import Session, select
from app.models import Reward, Quest, QuestCreate, RewardCreate
from app.core.cache import redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CACHE_EXPIRY = 300

def create_reward(*, session: Session, reward_create: RewardCreate) -> Reward:
    db_reward = Reward.model_validate(reward_create)
    session.add(db_reward)
    session.commit()
    session.refresh(db_reward)
    
    redis_client.delete(f"reward:{db_reward.reward_name}")
    redis_client.delete(f"reward:{db_reward.reward_id}")
    return db_reward

def get_reward_by_name(*, session: Session, reward_name: str) -> Reward | None:
    cache_key = f"reward:{reward_name}"
    
    cached_reward = redis_client.get(cache_key)
    if cached_reward:
        reward = Reward.model_validate(json.loads(cached_reward))
        logger.debug(f"reward {reward}")
        logger.info(f"Cache hit for reward {reward.reward_name}")
        return reward
    
    logger.info(f"Cache miss for reward {reward_name}")
    
    statement = select(Reward).where(Reward.reward_name == reward_name)
    session_reward = session.exec(statement).first()
    if session_reward:
        redis_client.set(cache_key, session_reward.model_dump_json(), ex=CACHE_EXPIRY)
    return session_reward

def get_reward_by_id(*, session: Session, reward_id: int) -> Reward | None:
    cache_key = f"reward:{reward_id}"
    
    cached_reward = redis_client.get(cache_key)
    if cached_reward:
        reward = Reward.model_validate(json.loads(cached_reward))
        logger.debug(f"reward {reward}")
        logger.info(f"Cache hit for reward {reward.reward_id}")
        return reward
    
    logger.info(f"Cache miss for reward {reward_id}")

    statement = select(Reward).where(Reward.reward_id == reward_id)
    session_reward = session.exec(statement).first()
    if session_reward:
        redis_client.set(cache_key, session_reward.model_dump_json(), ex=CACHE_EXPIRY)
    return session_reward

def create_quest(*, session: Session, quest_in: QuestCreate, reward_id: uuid.UUID) -> Quest:
    db_quest = Quest.model_validate(quest_in, update={"reward_id": reward_id})
    session.add(db_quest)
    session.commit()
    session.refresh(db_quest)
    
    redis_client.delete(f"quest:{db_quest.name}")
    redis_client.delete(f"quest:{db_quest.quest_id}")
    return db_quest

def get_quest_by_name(*, session: Session, name: str) -> Quest | None:
    cache_key = f"quest:{name}"
    
    cached_quest = redis_client.get(cache_key)
    if cached_quest:
        quest = Quest.model_validate(json.loads(cached_quest))
        logger.debug(f"quest {quest}")
        logger.info(f"Cache hit for quest {quest.name}")
        return quest
    
    logger.info(f"Cache miss for quest {name}")
    
    statement = select(Quest).where(Quest.name == name)
    session_quest = session.exec(statement).first()
    if session_quest:
        redis_client.set(cache_key, session_quest.model_dump_json(), ex=CACHE_EXPIRY)
    return session_quest

def get_quest_by_id(*, session: Session, quest_id: int) -> Quest | None:
    cache_key = f"quest:{quest_id}"
    
    cached_quest = redis_client.get(cache_key)
    if cached_quest:
        quest = Quest.model_validate(json.loads(cached_quest))
        logger.debug(f"quest {quest}")
        logger.info(f"Cache hit for quest {quest.quest_id}")
        return quest
    
    logger.info(f"Cache miss for quest {quest_id}")
    
    statement = select(Quest).where(Quest.quest_id == quest_id)
    session_quest = session.exec(statement).first()
    if session_quest:
        redis_client.set(cache_key, session_quest.model_dump_json(), ex=CACHE_EXPIRY)
    return session_quest
