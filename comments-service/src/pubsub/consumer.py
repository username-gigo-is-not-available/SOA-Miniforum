import json
from aiokafka import AIOKafkaConsumer
from fastapi.logger import logger
from src.settings import environment_variables_dict, set_connection_string
from src.pubsub.handlers import *
from src.pubsub.config import *

consumer: AIOKafkaConsumer | None = None

HANDLERS_MAP = {
    POST_DELETED_TOPIC: post_deleted_handler,
    POST_CREATED_TOPIC: post_created_handler,
    LIST_ALL_POSTS_TOPIC: list_all_posts_handler,
    USER_DELETED_TOPIC: user_deleted_handler,
    USER_CREATED_TOPIC: user_created_handler,
    LIST_ALL_USERS_TOPIC: list_all_users_handler
}


def get_consumer() -> AIOKafkaConsumer:
    global consumer
    connection_string = set_connection_string(connection_string=environment_variables_dict["BOOTSTRAP_SERVER"])
    if not consumer:
        consumer = AIOKafkaConsumer(
            *TOPICS,
            bootstrap_servers=connection_string
        )
    return consumer


async def consume() -> None:
    consumer = get_consumer()
    await consumer.start()
    try:
        async for message in consumer:
            logger.info(
                f"New message - Topic: {message.topic} Partition: {message.partition} Offset: {message.offset} "
                f"Key: {message.key} Value: {message.value} Timestamp: {message.timestamp}",
            )
            await HANDLERS_MAP[message.topic](json.loads(message.value.decode('utf-8')))

    finally:
        await consumer.stop()
