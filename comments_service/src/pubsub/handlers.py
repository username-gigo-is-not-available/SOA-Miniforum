from fastapi import Depends
from starlette.concurrency import run_in_threadpool
from src import crud
from src.crud import *
from src.database import get_collection
from src.database_models import Comment, PyObjectId


async def log_message(topic: str, message: dict) -> str:
    return f"Received message {message} from topic: {topic}"


async def post_deleted_handler(message: dict) -> list[Comment]:
    post_comments = await comments_by_post(post_id=message['_id'], collection=Depends(get_collection),
                                           parameters=(0, int(2 ** 31) - 1, [], {}))
    return [await delete(comment_id=str(comment.id), collection=get_collection) for comment in
            post_comments]


async def list_comments_by_post_handler(message: dict) -> list[Comment]:
    return await comments_by_post(post_id=message['post_id'], collection=Depends(get_collection),
                                  parameters=(0, int(2 ** 31) - 1, [], {}))


async def post_created_handler(message: dict) -> Comment:
    logger.info(f"Post IDs in comment service: {posts_ids}")
    return await run_in_threadpool(crud.posts_ids.append(map(lambda x: x['_id'], message)))


async def list_all_posts_handler(message: dict) -> list[PyObjectId]:
    [crud.posts_ids.append(PyObjectId(value)) for key, value in message.items() if key == 'id']
    logger.info(f"Listing all posts: {posts_ids}")
    return crud.posts_ids
