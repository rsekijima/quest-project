import requests
import logging

from app.models import Event
from app.core.config import settings

logger = logging.getLogger(__name__)

def process_event(event: Event):
    event_type = event.event_type
    if event_type == "NewUserSignIn":
        quest_name = "UserSignIn"
        catalog_service_url = f"{settings.CATALOG_SERVICE_URL}/api/v1/quests/name/{quest_name}"
        try:
            response = requests.get(catalog_service_url)
            if response.status_code == 200:
                print(f"Response from catalog-service: {response.json()}")

            else:
                logger.warning(f"Failed to fetch data from catalog-service: {response}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling catalog-service: {e}")
            return

    if event_type == "UserSignIn":
        quest_name = "UserSignIn"
        catalog_service_url = f"{settings.CATALOG_SERVICE_URL}/api/v1/quests/name/{quest_name}"
        try:
            response = requests.get(catalog_service_url)
            if response.status_code == 200:
                print(f"Response from catalog-service: {response.json()}")
                
            else:
                logger.warning(f"Failed to fetch data from catalog-service: {response}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling catalog-service: {e}")
            return