import json

from fastapi import FastAPI
from src.api.users_api import router as users_router
from fastapi.logger import logger

from src.crud import query
from src.database import get_cache
from src.pubsub.config import LIST_ALL_USERS_TOPIC
from src.pubsub.producer import get_producer

app = FastAPI(title="Users Service", root_path="/user-management-service")
app.include_router(router=users_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup event")

    await get_producer().start()
    cache = await get_cache()
    users = await query(cache=cache)
    for user in users:
        data = json.dumps(user.dict()).encode('utf-8')
        logger.info(f"Sending key: {user.id} value: {user.dict()} to topic: {LIST_ALL_USERS_TOPIC}")
        await get_producer().send(
            topic=LIST_ALL_USERS_TOPIC,
            value=data
        )


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown event")
    await get_producer().stop()
