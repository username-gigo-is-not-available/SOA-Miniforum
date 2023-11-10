from src.settings import environment_variables_dict, set_connection_string
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient
from fastapi.logger import logger
from typing import Optional


async def connect_to_mongodb() -> AsyncIOMotorClient:
    connection_string = set_connection_string(environment_variables_dict["CONNECTION_STRING"])
    logger.info(f"Connection string set: {connection_string}")
    return AsyncIOMotorClient(connection_string)


async def get_collection() -> Optional[AsyncIOMotorCollection]:
    client = await connect_to_mongodb()
    return client[environment_variables_dict["DATABASE_NAME"]][environment_variables_dict["COLLECTION_NAME"]]
