import json
from typing import Any
from fastapi import HTTPException
from fastapi.logger import logger
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
from src.database_models import *
from src.exceptions import *
from src.schemas import NotificationCreate, NotificationUpdate

SORT_BY_TIMESTAMP_ASC: list[tuple[str, int]] = [('timestamp', -1)]

DEFAULT_PARAMETERS = (0, int(2 ** 31) - 1, SORT_BY_TIMESTAMP_ASC, {})


async def create(notification: NotificationCreate, collection: AsyncIOMotorCollection) -> Notification:
    data = notification.dict()
    result = await collection.insert_one(data)
    if (inserted_notification := await get(notification_id=result.inserted_id, collection=collection)) is not None:
        logger.info(f"Inserted notification: {inserted_notification}")
        return inserted_notification
    else:
        logger.exception(notification_not_created_message())
        raise HTTPException(status_code=404, detail=notification_not_created_message())


async def get(notification_id: str, collection: AsyncIOMotorCollection) -> Notification:
    if (notification := await collection.find_one({"_id": ObjectId(notification_id)})) is not None:
        logger.info(f"Fetched notification: {notification}")
        return Notification(**notification)
    else:
        logger.exception(notification_not_found_message(notification_id=notification_id))
        raise HTTPException(status_code=404, detail=notification_not_found_message(notification_id=notification_id))


async def update(notification_id: str, notification: NotificationUpdate,
                 collection: AsyncIOMotorCollection) -> Notification:
    data = notification.dict()
    if (result := await collection.find_one_and_update({"_id": ObjectId(notification_id)}, {"$set": data},
                                                       return_document=ReturnDocument.AFTER)) is not None:
        logger.info(f"Updated notification: {notification}")
        return Notification(**result)
    else:
        logger.exception(notification_not_found_message(notification_id=notification_id))
        raise HTTPException(status_code=404, detail=notification_not_found_message(notification_id=notification_id))


async def delete(notification_id: str, collection: AsyncIOMotorCollection) -> Notification:
    if (result := await collection.find_one_and_delete({"_id": ObjectId(notification_id)})) is not None:
        logger.info(f"Deleted notification: {result}")
        return Notification(**result)
    else:
        logger.exception(notification_not_found_message(notification_id=notification_id))
        raise HTTPException(status_code=404, detail=notification_not_found_message(notification_id=notification_id))


async def query(collection: AsyncIOMotorCollection,
                parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None]) -> list[Notification]:
    offset, limit, order_by, where = parameters
    cursor = collection.find(where).skip(offset).limit(limit)
    cursor = cursor.sort(order_by) if order_by else cursor
    result = [Notification(**doc) async for doc in cursor]
    logger.info(f"Queried notifications: {result}")
    return result


async def count(collection: AsyncIOMotorCollection,
                parameters: tuple[int, int, list[tuple[str, int]] | None, dict[str, Any] | None]) -> int:
    if (result := await query(collection=collection, parameters=parameters)) is not None:
        logger.info(f"Total notifications: {len(result)}")
        return len(result)
    else:
        logger.exception(empty_inbox_message())
        raise HTTPException(status_code=404, detail=empty_inbox_message())


async def notifications_by_user(user_id: int, collection: AsyncIOMotorCollection) -> list[Notification]:
    offset, limit, order_by, where = DEFAULT_PARAMETERS
    where = {"user_id": user_id}
    if (result := await query(collection=collection, parameters=(offset, limit, order_by, where))) is not None:
        logger.info(posts_by_user_message(user_id=user_id, posts=result))
        return result
    else:
        raise HTTPException(status_code=404, detail=user_has_not_posted_yet_message(user_id=user_id))


async def notifications_by_user_count(user_id: int, collection: AsyncIOMotorCollection) -> int:
    if (result := await notifications_by_user(user_id=user_id, collection=collection)) is not None:
        logger.info(count_posts_by_user_message(user_id=user_id, total_posts=len(result)))
        return len(result)
    else:
        raise HTTPException(status_code=404, detail=user_has_not_posted_yet_message(user_id=user_id))
