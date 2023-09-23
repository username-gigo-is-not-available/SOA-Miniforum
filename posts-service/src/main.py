import json
from fastapi import FastAPI, Request
from fastapi.logger import logger
from src.crud import query, DEFAULT_PARAMETERS
from src.database import get_collection
from src.api.posts_api import router as posts_router
from src.pubsub.producer import get_producer
from src.serializers import post_serializer
from src.pubsub.config import *

app = FastAPI(title="Posts Service")

app.include_router(posts_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup event")

    await get_producer().start()
    collection = await get_collection()
    posts = await query(collection=collection, parameters=DEFAULT_PARAMETERS)
    for post in posts:
        data = json.dumps(post_serializer(post=post)).encode('utf-8')
        logger.info(f"Sending key: {post.dict()['id']} value: {post.dict()} to topic: {LIST_ALL_POSTS_TOPIC}")
        await get_producer().send(
            topic=LIST_ALL_POSTS_TOPIC,
            value=data
        )


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown event")
    await get_producer().stop()


@app.middleware("http")
async def validate_jwt(request: Request, call_next):
    # request.get("Authorization")
    print(request.headers)
    response = await call_next(request)
    return response
