from redis.asyncio import Redis
from redis.asyncio import from_url
from src.settings import environment_variables_dict, set_connection_string
from fastapi.logger import logger


async def connect_to_redis() -> Redis:
    connection_string = set_connection_string(environment_variables_dict["CONNECTION_STRING"])
    logger.info(f"Redis connection string set: {connection_string}")
    return await from_url(connection_string, decode_responses=True)


async def get_cache() -> Redis:
    return await connect_to_redis()


