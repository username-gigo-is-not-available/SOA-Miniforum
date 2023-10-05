import json
from typing import Any
from fastapi import HTTPException
from fastapi.logger import logger
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
from src.database_models import *
from src.exceptions import *
from src.pubsub.config import POST_DELETED_TOPIC, POST_CREATED_TOPIC
from src.pubsub.producer import get_producer
from src.schemas import PostCreate, PostUpdate
from src.serializers import post_serializer

SORT_BY_TIMESTAMP_ASC: list[tuple[str, int]] = [('timestamp', -1)]

DEFAULT_PARAMETERS = (0, int(2 ** 31) - 1, SORT_BY_TIMESTAMP_ASC, {})


async def create(post: PostCreate, collection: AsyncIOMotorCollection) -> Post:
    data = post.dict()
    data['timestamp'] = datetime.now()
    result = await collection.insert_one(data)
    if (inserted_post := await get(post_id=result.inserted_id, collection=collection)) is not None:
        logger.info(f"Inserted post: {inserted_post}")
        data = json.dumps(post_serializer(post=inserted_post)).encode('utf-8')
        logger.info(
            f"Sending key: {inserted_post.dict()['id']} value: {inserted_post.dict()} to topic: {POST_CREATED_TOPIC}")
        await get_producer().send(topic=POST_CREATED_TOPIC,
                                  value=data
                                  )
        return inserted_post
    else:
        logger.exception(post_not_created_message())
        raise HTTPException(status_code=404, detail=post_not_created_message())


async def get(post_id: str, collection: AsyncIOMotorCollection) -> Post:
    if (post := await collection.find_one({"_id": ObjectId(post_id)})) is not None:
        logger.info(f"Fetched post: {post}")
        return Post(**post)
    else:
        logger.exception(post_not_found_message(post_id=post_id))
        raise HTTPException(status_code=404, detail=post_not_found_message(post_id=post_id))


async def update(post_id: str, post: PostUpdate, collection: AsyncIOMotorCollection) -> Post:
    data = post.dict()
    data['timestamp'] = datetime.now()
    if (result := await collection.find_one_and_update({"_id": ObjectId(post_id)}, {"$set": data},
                                                       return_document=ReturnDocument.AFTER)) is not None:
        logger.info(f"Updated post: {post}")
        return Post(**result)
    else:
        logger.exception(post_not_found_message(post_id=post_id))
        raise HTTPException(status_code=404, detail=post_not_found_message(post_id=post_id))


async def delete(post_id: str, collection: AsyncIOMotorCollection) -> Post:
    if (result := await collection.find_one_and_delete({"_id": ObjectId(post_id)})) is not None:
        logger.info(f"Deleted post: {result}")
        data = json.dumps(post_serializer(post=Post(**result))).encode('utf-8')
        logger.info(f"Sending key: {result['_id']} value: {result} to topic: {POST_DELETED_TOPIC}")
        await get_producer().send(topic=POST_DELETED_TOPIC,
                                  value=data
                                  )
        return Post(**result)
    else:
        logger.exception(post_not_found_message(post_id=post_id))
        raise HTTPException(status_code=404, detail=post_not_found_message(post_id=post_id))


async def query(collection: AsyncIOMotorCollection,
                parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None]) -> list[Post]:
    offset, limit, order_by, where = parameters
    cursor = collection.find(where).skip(offset).limit(limit)
    cursor = cursor.sort(order_by) if order_by else cursor
    result = [Post(**doc) async for doc in cursor]
    logger.info(f"Queried posts: {result}")
    return result


async def count(collection: AsyncIOMotorCollection,
                parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None]) -> int:
    if (result := await query(collection=collection, parameters=parameters)) is not None:
        logger.info(f"Total posts: {len(result)}")
        return len(result)
    else:
        logger.exception(no_active_posts_message())
        raise HTTPException(status_code=404, detail=no_active_posts_message())


async def posts_by_user(user_id: int, collection: AsyncIOMotorCollection) -> list[Post]:
    offset, limit, order_by, where = DEFAULT_PARAMETERS
    where = {"user_id": user_id}
    if (result := await query(collection=collection, parameters=(offset, limit, order_by, where))) is not None:
        logger.info(posts_by_user_message(user_id=user_id, posts=result))
        return result
    else:
        raise HTTPException(status_code=404, detail=user_has_not_posted_yet_message(user_id=user_id))


async def posts_by_user_count(user_id: int, collection: AsyncIOMotorCollection) -> int:
    if (result := await posts_by_user(user_id=user_id, collection=collection)) is not None:
        logger.info(count_posts_by_user_message(user_id=user_id, total_posts=len(result)))
        return len(result)
    else:
        raise HTTPException(status_code=404, detail=user_has_not_posted_yet_message(user_id=user_id))
