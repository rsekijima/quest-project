import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.core.config import settings
from app.models import Quest, Reward

def fetch_quest_by_id(quest_id: str) -> Quest | None:
    """
    Fetch quest data from the catalog service
    """
    catalog_service_url = f"{settings.CATALOG_SERVICE_URL}/api/v1/quests/{quest_id}"
    try:
        response = requests.get(catalog_service_url)
        quest = Quest(**response.json())
        return quest
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return None
    
    
def fetch_reward_by_id(reward_id: str) -> Reward | None:
    """
    Fetch reward data from the catalog service
    """
    catalog_service_url = f"{settings.CATALOG_SERVICE_URL}/api/v1/rewards/{reward_id}"
    try:
        response = requests.get(catalog_service_url)
        reward = Reward(**response.json())
        return reward
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return None
    
