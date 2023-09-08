from fastapi.logger import logger
from src import database
from src.crud import *
from src.database_models import Comment


def log_message(topic: str, message: dict) -> str:
    return f"Received message {message} from topic: {topic}"


def list_all_posts_message(post_ids: list[str]):
    return f"Listing all posts: {post_ids}"


async def post_deleted_handler(message: dict) -> list[Comment]:
    logger.info(log_message(settings.POST_DELETED_TOPIC, message))
    post_comments = await comments_by_post(post_id=str(message['id']), collection=await database.get_collection())
    result = []
    for comment in post_comments:
        deleted_comment = await delete(comment_id=str(comment.id), collection=await database.get_collection())
        result.append(deleted_comment)
    settings.post_ids.remove(str(message['id']))
    logger.info(list_all_posts_message(post_ids=settings.post_ids))
    return result


async def post_created_handler(message: dict) -> list[Comment]:
    logger.info(log_message(settings.POST_CREATED_TOPIC, message))
    settings.post_ids.append(str(message['id']))
    logger.info(list_all_posts_message(post_ids=settings.post_ids))
    return await comments_by_post(post_id=str(message['id']), collection=await database.get_collection())


async def list_all_posts_handler(message: dict) -> list[str]:
    logger.info(log_message(settings.LIST_ALL_POSTS_TOPIC, message))
    [settings.post_ids.append(str(value)) for key, value in message.items() if key == 'id']
    logger.info(list_all_posts_message(post_ids=settings.post_ids))
    return settings.post_ids
