import aio_pika
import json
import logging

from app.core.config import settings
from app.models import Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def rabbitmq_consumer(queue_name: str = "user_events"):
    """Function to consume messages from RabbitMQ."""
    connection = await aio_pika.connect_robust(settings.RABBITMQ)
    channel = await connection.channel()

    queue = await channel.declare_queue(queue_name)

    async def on_message(message: aio_pika.IncomingMessage):
        async with message.process():
            data = json.loads(json.loads(message.body))
            event = Event(**data)
            logger.info(f"Received event: {event}")

            

    await queue.consume(on_message, no_ack=False)
