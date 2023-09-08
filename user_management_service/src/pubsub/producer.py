from asyncio import get_event_loop

from aiokafka import AIOKafkaProducer

from src.settings import set_connection_string, environment_variables_dict

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
