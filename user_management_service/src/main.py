from fastapi import FastAPI
from src.api.users_api import router as users_router

app = FastAPI(title="Users Service")
app.include_router(router=users_router)

