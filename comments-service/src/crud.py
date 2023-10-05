from typing import Any
from fastapi import HTTPException
from fastapi.logger import logger
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from src import settings
from src.database_models import *
from src.exceptions import *
from src.schemas import CommentCreate, CommentUpdate


SORT_BY_TIMESTAMP_ASC: list[tuple[str, int]] = [('timestamp', -1)]

DEFAULT_PARAMETERS = (0, int(2 ** 31) - 1, SORT_BY_TIMESTAMP_ASC, {})


async def check_if_valid_post_id(post_id: str):
    logger.info(f"Checking if post with post_id {post_id} exists in {settings.post_ids}")
    return post_id in settings.post_ids


async def create(comment: CommentCreate, collection: AsyncIOMotorCollection) -> Comment:
    data = comment.dict()
    data['timestamp'] = datetime.now()
    post_exists = await check_if_valid_post_id(post_id=str(data['post_id']))
    logger.info(f"Post with post_id: {data['post_id']} exists? {post_exists}")
    if not post_exists:
        logger.exception(post_not_found_message(post_id=data['post_id']))
        raise HTTPException(status_code=404, detail=post_not_found_message(post_id=data['post_id']))
    result = await collection.insert_one(data)
    if (inserted_post := await get(comment_id=result.inserted_id, collection=collection)) is not None:
        logger.info(f"Inserted comment: {inserted_post}")
        return inserted_post
    else:
        logger.exception(comment_not_created_message())
        raise HTTPException(status_code=404, detail=comment_not_created_message())


async def get(comment_id: str, collection: AsyncIOMotorCollection) -> Comment:
    if (result := await collection.find_one({"_id": ObjectId(comment_id)})) is not None:
        logger.info(f"Fetched comment: {result}")
        return Comment(**result)
    else:
        logger.exception(comment_not_found_message(comment_id=comment_id))
        raise HTTPException(status_code=404, detail=comment_not_found_message(comment_id=comment_id))


async def update(comment_id: str, comment: CommentUpdate, collection: AsyncIOMotorCollection) -> Comment:
    data = comment.dict()
    data['timestamp'] = datetime.now()
    if (result := await collection.find_one_and_update({"_id": ObjectId(comment_id)}, {"$set": data},
                                                       return_document=ReturnDocument.AFTER)) is not None:
        logger.info(f"Updated comment: {result}")
        return Comment(**result)
    else:
        logger.exception(comment_not_found_message(comment_id=comment_id))
        raise HTTPException(status_code=404, detail=comment_not_found_message(comment_id=comment_id))


async def delete(comment_id: str, collection: AsyncIOMotorCollection) -> Comment:
    if (result := await collection.find_one_and_delete({"_id": ObjectId(comment_id)})) is not None:
        logger.info(f"Deleted comment: {result}")
        return Comment(**result)
    else:
        logger.exception(comment_not_found_message(comment_id=comment_id))
        raise HTTPException(status_code=404, detail=comment_not_found_message(comment_id=comment_id))


async def query(collection: AsyncIOMotorCollection,
                parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None]) -> list[Comment]:
    offset, limit, order_by, where = parameters
    cursor = collection.find(where).skip(offset).limit(limit)
    cursor = cursor.sort(order_by) if order_by else cursor
    result = [Comment(**doc) async for doc in cursor]
    return result


async def count(collection: AsyncIOMotorCollection,
                parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None]) -> int:
    if (result := await query(collection=collection, parameters=parameters)) is not None:
        logger.info(f"Total comments: {len(result)}")
        return len(result)
    else:
        logger.exception(comments_not_found_message())
        raise HTTPException(status_code=404, detail=comments_not_found_message())


async def comments_by_user(user_id: int, collection: AsyncIOMotorCollection) -> \
        list[Comment]:
    offset, limit, order_by, where = DEFAULT_PARAMETERS
    where = {"user_id": user_id}
    order_by = SORT_BY_TIMESTAMP_ASC
    if (result := await query(collection=collection, parameters=(offset, limit, order_by, where))) is not None:
        logger.info(comments_by_user_message(user_id=user_id, comments=result))
        return result
    else:
        raise HTTPException(status_code=404, detail=user_has_not_commented_yet_message(user_id=user_id))


async def comments_by_user_count(user_id: int, collection: AsyncIOMotorCollection) -> int:
    if (result := await comments_by_user(user_id=user_id, collection=collection)) is not None:
        logger.info(total_comments_by_user_message(user_id=user_id, total_comments=len(result)))
        return len(result)
    else:
        raise HTTPException(status_code=404, detail=comments_not_found_message())


async def comments_by_post(post_id: str, collection: AsyncIOMotorCollection) -> \
        list[Comment]:
    offset, limit, order_by, where = DEFAULT_PARAMETERS
    where = {"post_id": ObjectId(post_id)}
    order_by = SORT_BY_TIMESTAMP_ASC
    if (result := await query(collection=collection, parameters=(offset, limit, order_by, where))) is not None:
        logger.info(post_has_comments_message(post_id=post_id, comments=result))
        return result
    else:
        raise HTTPException(status_code=404, detail=post_has_no_comments_message(post_id=post_id))


async def comments_by_post_count(post_id: str, collection: AsyncIOMotorCollection) -> int:
    if (comments := await comments_by_post(post_id=post_id, collection=collection)) is not None:
        logger.info(post_has_total_comments_message(post_id=post_id, total_comments=len(comments)))
        return len(comments)
    else:
        raise HTTPException(status_code=404, detail=post_has_no_comments_message(post_id=post_id))
