import aio_pika
import json
import logging

from app.core.config import settings
from app.models import EventPublish, Event
from app.service.events import process_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQClient:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ)
        self.channel = await self.connection.channel()

    async def publish(self, event: EventPublish, publish_queue: str):
        if not self.channel:
            await self.connect()

        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(event.model_dump_json()).encode("utf-8")),
            routing_key=publish_queue,
        )
        logger.info(f"Published event: {event}")

    async def consume(self):
        if not self.channel:
            await self.connect()

        queue = await self.channel.declare_queue(self.queue_name)

        async def on_message(message: aio_pika.IncomingMessage):
            async with message.process():
                data = json.loads(json.loads(message.body))
                event = Event(**data)
                logger.info(f"Received event: {event}")
                await process_event(event=event)

        await queue.consume(on_message, no_ack=False)

rabbitmq_client = RabbitMQClient(queue_name="auth-events")