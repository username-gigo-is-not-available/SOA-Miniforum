from asyncio import get_event_loop
from aiokafka import AIOKafkaProducer
from src.settings import environment_variables_dict, set_connection_string

POST_DELETED_TOPIC: str = environment_variables_dict["POST_DELETED_TOPIC"]
GET_COMMENTS_FOR_POST: str = environment_variables_dict["GET_COMMENTS_FOR_POST_TOPIC"]
POST_CREATED_TOPIC: str = environment_variables_dict["POST_CREATED_TOPIC"]
LIST_ALL_POSTS_TOPIC: str = environment_variables_dict["LIST_ALL_POSTS_TOPIC"]

TOPICS: list = [POST_DELETED_TOPIC, GET_COMMENTS_FOR_POST, POST_CREATED_TOPIC, LIST_ALL_POSTS_TOPIC]

producer: AIOKafkaProducer | None = None


def get_producer() -> AIOKafkaProducer:
    global producer
    connection_string = set_connection_string(environment_variables_dict["BOOTSTRAP_SERVER"])
    if not producer:
        producer = AIOKafkaProducer(
            loop=get_event_loop(),
            bootstrap_servers=connection_string
        )
    return producer
