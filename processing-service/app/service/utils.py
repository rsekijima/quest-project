import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.core.config import settings
from app.models import Quest

def fetch_quest(quest_name: str) -> Quest | None:
    """
    Fetch quest data from the catalog service
    """
    catalog_service_url = f"{settings.CATALOG_SERVICE_URL}/api/v1/quests/name/{quest_name}"
    try:
        response = requests.get(catalog_service_url)
        quest = Quest(**response.json())
        return quest
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return None