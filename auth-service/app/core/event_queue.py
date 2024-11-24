import pika
import json
from app.core.config import settings
from app.models import Event
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def publish_event(event: Event, queue_name: str = "user_events"):
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ))
    channel = connection.channel()

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(event.model_dump_json()),
        properties=pika.BasicProperties(content_type="application/json"),
    )

    logger.info(f"Published event to {queue_name}: {event}")
    connection.close()