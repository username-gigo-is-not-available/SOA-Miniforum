import re
from datetime import datetime

from fastapi import HTTPException
from fastapi.logger import logger
from redis.asyncio import Redis
from starlette.responses import RedirectResponse

from src import auth
from src.database_models import User
from src.exceptions import user_not_found_message, email_already_taken_message
from src.schemas import UserCreate, UserUpdate


def get_user_hash_name(user_id: int) -> str:
    return f"user:{user_id}"


async def create(user: UserCreate, cache: Redis) -> User:
    try:
        if await find_user_by_email(email=user.email, cache=cache):
            logger.exception(email_already_taken_message(email=user.email))
            raise HTTPException(status_code=400, detail=email_already_taken_message(email=user.email))
    except HTTPException as e:
        if e.status_code == 404:
            data = user.dict()
            data['hashed_password'] = auth.hash_password(password=user.password)
            data['timestamp'] = int(datetime.now().timestamp())
            data.pop('password')
            user_id = await cache.incr("user_count")
            logger.info(f"Created user: {user} with id {user_id}")
            result = User(**data, id=user_id)
            await cache.hset(name=get_user_hash_name(user_id=user_id), mapping=result.dict())
            return result


async def get(user_id: int, cache: Redis) -> User:
    user = await cache.hgetall(name=get_user_hash_name(user_id=user_id))
    if user:
        logger.info(f"Fetched user: {user}")
        return User(**user)
    else:
        logger.exception(user_not_found_message(user_id=user_id))
        raise HTTPException(status_code=404, detail=user_not_found_message(user_id=user_id))


async def update(user_id: int, user_update: UserUpdate, cache: Redis) -> User:
    if (user_exists := await get(user_id=user_id, cache=cache)) is not None:
        user = user_exists.dict()
        user['hashed_password'] = auth.hash_password(password=user_update.password)
        user['email'] = user_update.email
        user['timestamp'] = int(datetime.now().timestamp())
        await cache.hset(name=get_user_hash_name(user_id=user_id), mapping=user)
        logger.info(f"Updated user: {user_update}")
        return User(**user)
    else:
        logger.exception(user_not_found_message(user_id=user_id))
        raise HTTPException(status_code=404, detail=user_not_found_message(user_id=user_id))


async def delete(user_id: int, cache: Redis) -> User:
    user = await cache.hgetall(get_user_hash_name(user_id=user_id))
    if user and await cache.hdel(get_user_hash_name(user_id=user_id), *user.keys()) > 0:
        logger.info(f"Deleted user: {user}")
        return User(**user)
    else:
        logger.exception(user_not_found_message(user_id=user_id))
        raise HTTPException(status_code=404, detail=user_not_found_message(user_id=user_id))


async def query(cache: Redis, email_pattern: str | None = None) -> list[User]:
    result = []
    for key in await cache.keys("user:*"):
        data = await cache.hgetall(name=key)
        result.append(User(**data)) if re.search(email_pattern, data['email']) else None
    logger.info(f"Queried users: {result}")
    return result


async def find_user_by_email(email: str | None, cache: Redis) -> User:
    users = await cache.keys("user:*")
    for user in users:
        data = await cache.hgetall(name=user)
        if data['email'] == email:
            logger.info(f"Found user: {data} by email: {email}")
            return User(**data)
    logger.info(user_not_found_message(email=email))
    logger.exception(user_not_found_message(email=email))
    raise HTTPException(status_code=404, detail=user_not_found_message(email=email))


def redirect_to_gateway(token: str) -> RedirectResponse:
    url = "http://localhost:8000/posts-service/docs"
    headers = {"Authorization": f"Bearer {token}"}
    return RedirectResponse(url=url, headers=headers)
