from fastapi import FastAPI
from fastapi.logger import logger
from asyncio import get_event_loop
from src.api.comments_api import router as comments_router
from src.pubsub.consumer import *

app = FastAPI(title="Comments Service")

app.include_router(comments_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup event")
    event_loop = get_event_loop()
    event_loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown event")
    consumer = get_consumer()
    await consumer.stop()
