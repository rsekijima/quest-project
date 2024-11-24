import requests
import logging

from sqlmodel import Session
from datetime import datetime


from app.core.db import engine
from app.models import Event
from app.core.config import settings
from app.crud import create_user_quest_reward, get_user_quest_reward_by_user_id_quest_id, update_user_quest_reward, create_event
from app.models import UserQuestRewardCreate, UserQuestRewardUpdate, Quest, UserQuestReward, EventCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_quest(quest_name: str) -> Quest | None:
    catalog_service_url = f"{settings.CATALOG_SERVICE_URL}/api/v1/quests/name/{quest_name}"
    try:
        response = requests.get(catalog_service_url)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling catalog-service: {e}")
        return None

def verify_quest_completed(quest: Quest, user_quest_reward: UserQuestReward):
    return user_quest_reward.duplication == quest.duplication

def can_receive_reward(quest: Quest, user_quest_reward: UserQuestReward):
    return user_quest_reward.streak == quest.streak and user_quest_reward.duplication < quest.duplication

def create_or_update_user_quest_reward(session: Session, event: Event, quest: Quest, is_new_user: bool) -> UserQuestReward | None:
    if is_new_user:
        user_quest_reward_create = UserQuestRewardCreate(user_id=event.user_id, quest_id=quest.quest_id, status=0, streak=1, duplication=0)
        user_quest_reward = create_user_quest_reward(session=session, user_quest_reward_create=user_quest_reward_create)
    else:
        user_quest_reward = get_user_quest_reward_by_user_id_quest_id(session=session, user_id=event.user_id, quest_id=quest.quest_id)
        logger.info(f"user_quest_reward: {user_quest_reward}")

        if not user_quest_reward:
            logger.warning(f"No existing user quest reward found for user_id={event.user_id} and quest_id={quest.quest_id}")
            return None

        if verify_quest_completed(quest=quest,user_quest_reward=user_quest_reward):
            logger.info(f"user {event.user_id} already completed quest {quest.name}")
            return user_quest_reward
        
        user_quest_reward_update = UserQuestRewardUpdate(streak=user_quest_reward.streak + 1)
        logger.info(f"user_quest_reward_update: {user_quest_reward_update}")
        user_quest_reward = update_user_quest_reward(session=session, db_user_quest_reward=user_quest_reward, user_quest_reward_update=user_quest_reward_update)

    
    logger.info(f"updated user_quest_reward: {user_quest_reward}")
    return user_quest_reward

def reset_streak(session: Session, user_quest_reward: UserQuestReward) -> UserQuestReward:
    user_quest_reward_update = UserQuestRewardUpdate(streak=0,duplication=user_quest_reward.duplication+1)
    user_quest_reward = update_user_quest_reward(session=session, db_user_quest_reward=user_quest_reward, user_quest_reward_update=user_quest_reward_update)
    return


def process_event(event: Event):

    quest_name = "UserSignIn"
    quest_data = fetch_quest(quest_name)
    if not quest_data:
        return

    quest = Quest(**quest_data)
    
    with Session(engine) as session:

        create_event(session=session, event_create=event)
        event_type = event.event_type
        logger.info(f"Event_type: {event_type}")

        if event_type == "NewUserSignIn":
            logger.info(f"Processing NewUserSignIn for user_id={event.user_id}")
            user_quest_reward = create_or_update_user_quest_reward(session=session, event=event, quest=quest, is_new_user=True)

        elif event_type == "UserSignIn":
            logger.info(f"Processing UserSignIn for user_id={event.user_id}")
            user_quest_reward = create_or_update_user_quest_reward(session=session, event=event, quest=quest, is_new_user=False)
        
        if user_quest_reward and can_receive_reward(quest=quest,user_quest_reward=user_quest_reward):
            reset_streak(session=session, user_quest_reward=user_quest_reward)
            quest_complete_event_create = EventCreate(event_type="QuestCompleted", user_id=event.user_id,timestamp=datetime.now(), event_data={"quest_id": str(quest.quest_id)})
            create_event(session=session, event_create=quest_complete_event_create)


