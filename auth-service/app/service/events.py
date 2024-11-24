import logging
import uuid

from app.models import Event, EventClaimCreate
from sqlmodel import Session

from app.core.db import engine
from app.crud import create_event_claim
from app.service.utils import fetch_quest_by_id, fetch_reward_by_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_quest_completed_event(session: Session, event: Event):
    """
    Process QuestComplete event,
    """
    try:
        quest_id = uuid.UUID(event.event_data["quest_id"])
    except ValueError:
        logger.error("Failed to process event: Invalid quest ID")
        return
    
    quest = fetch_quest_by_id(quest_id=quest_id)
    logger.info(f"quest {quest}")
    if not quest:
        logger.error("Quest with ID {quest_id} not found")
        return

    reward = fetch_reward_by_id(reward_id=quest.reward_id)
    logger.info(f"reward {reward}")
    if not reward:
        logger.error("Reward with ID {reward_id} not found")
        return

    event_claim_create = EventClaimCreate(user_id=event.user_id,quest_id=quest.quest_id,reward_item=reward.reward_item,reward_qty=reward.reward_qty)
    create_event_claim(session=session,event_claim_create=event_claim_create)
    return

EVENT_HANDLER = {"QuestCompleted": process_quest_completed_event}

async def process_event(event: Event):

    with Session(engine) as session:
        event_type = event.event_type
        logger.info(f"Received event of type: {event_type}")

        if event_type in EVENT_HANDLER:
            await EVENT_HANDLER[event_type](session=session,event=event)
        else:
            logger.warning(f"Event handler not implemented for {event_type}")