import logging

from sqlmodel import Session
from datetime import datetime

from app.core.db import engine
from app.models import Event
from app.crud import create_user_quest_reward, get_user_quest_reward_by_user_id_quest_id, update_user_quest_reward, create_event
from app.models import UserQuestRewardCreate, UserQuestRewardUpdate, Quest, UserQuestReward, EventPublish
from app.service.utils import fetch_quest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUEST_NAME = "UserSignIn"

def verify_quest_completed(quest: Quest, user_quest_reward: UserQuestReward):
    """
    Verify if user already completed the limit of times a certain quest can be completed
    """
    return user_quest_reward.duplication == quest.duplication

def completed_streak(quest: Quest, user_quest_reward: UserQuestReward):
    """
    Verify if the user progress already reach the required streak
    """
    return user_quest_reward.streak == quest.streak and user_quest_reward.duplication < quest.duplication

def update_user_progress(session: Session, user_quest_reward: UserQuestReward) -> UserQuestReward:
    """
    Update the progress of a user in a quest (reset the streak and increase the duplication vlaue)
    """
    user_quest_reward_update = UserQuestRewardUpdate(streak=0,duplication=user_quest_reward.duplication+1)
    user_quest_reward = update_user_quest_reward(session=session, db_user_quest_reward=user_quest_reward, user_quest_reward_update=user_quest_reward_update)
    return

async def process_new_user_sign_in_event(session: Session, event: Event):
    """
    Process the event NewUserSignin
    """

    quest = fetch_quest(QUEST_NAME)
    if not quest:
        logger.warning(f"Quest {QUEST_NAME} not found")
        return
    
    user_quest_reward_create = UserQuestRewardCreate(user_id=event.user_id, quest_id=quest.quest_id, status=0, streak=1, duplication=0)
    user_quest_reward = create_user_quest_reward(session=session, user_quest_reward_create=user_quest_reward_create)
    
    if completed_streak(quest=quest,user_quest_reward=user_quest_reward):
        await send_quest_complete_event(session=session, event=event, quest=quest,user_quest_reward=user_quest_reward)

async def process_user_sign_in_event(session: Session, event: Event):
    """
    Process the event UserSignin
    """

    quest = fetch_quest(QUEST_NAME)
    if not quest:
        logger.warning(f"Quest {QUEST_NAME} not found")
        return
    
    user_quest_reward = get_user_quest_reward_by_user_id_quest_id(session=session, user_id=event.user_id, quest_id=quest.quest_id)
    
    if not user_quest_reward:
        logger.warning(f"No existing user quest reward found for user_id={event.user_id} and quest_id={quest.quest_id}")
        return
    
    if verify_quest_completed(quest=quest,user_quest_reward=user_quest_reward):
        logger.info(f"user {event.user_id} already completed quest {quest.name}")
        return
            
    user_quest_reward_update = UserQuestRewardUpdate(streak=user_quest_reward.streak + 1)
    user_quest_reward = update_user_quest_reward(session=session, db_user_quest_reward=user_quest_reward, user_quest_reward_update=user_quest_reward_update)

    if completed_streak(quest=quest,user_quest_reward=user_quest_reward):
        await send_quest_complete_event(session=session, event=event, quest=quest,user_quest_reward=user_quest_reward)

async def send_quest_complete_event(session: Session, event: Event, quest: Quest, user_quest_reward: UserQuestReward):
    """
    Sends a QuestCompleted event if the user reach the required streak for an event
    """
    from app.core.event_queue import rabbitmq_client

    update_user_progress(session=session, user_quest_reward=user_quest_reward)
    
    quest_complete_event_publish = EventPublish(event_type="QuestCompleted", user_id=event.user_id,timestamp=datetime.now(), event_data={"quest_id": str(quest.quest_id)})
    await rabbitmq_client.publish(event=quest_complete_event_publish, publish_queue="processing-events")
    await rabbitmq_client.publish(event=quest_complete_event_publish, publish_queue="auth-events")

EVENT_HANDLER = {"NewUserSignIn": process_new_user_sign_in_event, "UserSignIn": process_user_sign_in_event}

async def process_event(event: Event):
    """
    Process quest events from the event queue
    """

    with Session(engine) as session:
        create_event(session=session, event_create=event)
        event_type = event.event_type
        logger.info(f"Received event of type: {event_type}")

        if event_type in EVENT_HANDLER:
            await EVENT_HANDLER[event_type](session=session,event=event)
        else:
            logger.warning(f"Event handler not implemented for {event_type}")
