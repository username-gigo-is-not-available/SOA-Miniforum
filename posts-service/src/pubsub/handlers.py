from fastapi.logger import logger
from src import database, settings
from src.crud import *
from src.database_models import Post
from src.pubsub import config


def log_message(topic: str, message: dict) -> str:
    return f"Received message {message} from topic: {topic}"


def list_all_users_message(user_ids: list[int]):
    return f"Listing all users: {user_ids}"


async def user_created_handler(message: dict) -> list[Post]:
    logger.info(log_message(config.USER_CREATED_TOPIC, message=message))
    settings.user_ids.append(message['id'])
    logger.info(list_all_users_message(user_ids=settings.user_ids))
    return await posts_by_user(user_id=message['id'], collection=await database.get_collection())


async def user_deleted_handler(message: dict) -> list[Post]:
    logger.info(log_message(config.USER_DELETED_TOPIC, message))
    user_posts = await posts_by_user(user_id=message['id'], collection=await database.get_collection())
    result = []
    for post in user_posts:
        deleted_post = await delete(post_id=str(post.id), collection=await database.get_collection())
        result.append(deleted_post)
    settings.user_ids.remove(message['id'])
    logger.info(list_all_users_message(user_ids=settings.user_ids))
    return result


async def list_all_users_handler(message: dict) -> list[int]:
    logger.info(log_message(config.LIST_ALL_USERS_TOPIC, message))
    [settings.user_ids.append(value) for key, value in message.items() if key == 'id']
    logger.info(list_all_users_message(user_ids=settings.user_ids))
    return settings.user_ids
