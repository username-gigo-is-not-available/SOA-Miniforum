import re

from fastapi import HTTPException
from fastapi.logger import logger
from redis.asyncio import Redis

from src import auth
from src.database_models import User
from src.exceptions import user_not_found_message, email_already_taken_message
from src.schemas import UserCreate, UserUpdate


# bottleneck?
def get_user_hash_name(user_id: int):
    return f"user:{user_id}"


async def create(user: UserCreate, db: Redis) -> User:
    try:
        if await find_user_by_email(email=user.email, db=db):
            raise HTTPException(status_code=400, detail=email_already_taken_message(email=user.email))
    except HTTPException as e:
        if e.status_code == 404:
            data = user.dict()
            data['hashed_password'] = auth.hash_password(password=user.password)
            data.pop('password')
            user_id = await db.incr("user_count")
            logger.info(f"Created user: {user} with id {user_id}")
            result = User(**data, id=user_id)
            await db.hset(name=get_user_hash_name(user_id=user_id), mapping=result.dict())
            return result


async def get(user_id: int, db: Redis) -> User:
    user = await db.hgetall(name=get_user_hash_name(user_id=user_id))
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail=user_not_found_message(user_id=user_id))


async def update(user_id: int, user: UserUpdate, db: Redis) -> User:
    data = user.dict()
    data['id'] = user_id
    data['hashed_password'] = auth.hash_password(password=user.password)
    data.pop('password')
    await db.hset(name=get_user_hash_name(user_id=user_id), mapping=data)
    return User(**data)


async def delete(user_id: int, db: Redis) -> User:
    user_data = await db.hgetall(get_user_hash_name(user_id=user_id))
    if user_data and await db.hdel(get_user_hash_name(user_id=user_id), *user_data.keys()) > 0:
        return User(**user_data)
    else:
        raise HTTPException(status_code=404, detail=user_not_found_message(user_id=user_id))


async def query(db: Redis, email_pattern: str = None) -> list[User]:
    result = []
    for key in await db.keys("user:*"):
        data = await db.hgetall(name=key)
        result.append(User(**data)) if re.search(email_pattern, data['email']) else None

    return result


async def find_user_by_email(email: str, db: Redis) -> User:
    users = await db.keys("user:*")
    for user in users:
        data = await db.hgetall(name=user)
        if data['email'] == email:
            return User(**data)
    raise HTTPException(status_code=404, detail=user_not_found_message(email=email))
