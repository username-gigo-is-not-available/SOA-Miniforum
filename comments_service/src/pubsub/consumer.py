import json

from aiokafka import AIOKafkaConsumer
from fastapi.logger import logger
from src.settings import environment_variables_dict, set_connection_string
from src.pubsub.handlers import *

POST_DELETED_TOPIC: str = environment_variables_dict["POST_DELETED_TOPIC"]
GET_COMMENTS_FOR_POST: str = environment_variables_dict["GET_COMMENTS_FOR_POST_TOPIC"]
POST_CREATED_TOPIC: str = environment_variables_dict["POST_CREATED_TOPIC"]
LIST_ALL_POSTS_TOPIC: str = environment_variables_dict["LIST_ALL_POSTS_TOPIC"]

TOPICS: list = [POST_DELETED_TOPIC, GET_COMMENTS_FOR_POST, POST_CREATED_TOPIC, LIST_ALL_POSTS_TOPIC]
consumer: AIOKafkaConsumer | None = None

HANDLERS_MAP = {
    POST_DELETED_TOPIC: post_deleted_handler,
    GET_COMMENTS_FOR_POST: list_comments_by_post_handler,
    POST_CREATED_TOPIC: post_created_handler,
    LIST_ALL_POSTS_TOPIC: list_all_posts_handler

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
