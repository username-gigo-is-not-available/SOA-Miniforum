from fastapi import APIRouter, HTTPException, Depends

from auth import AuthHandler
from database_models import User
from schemas import UserCreate, UserBase

auth_handler = AuthHandler()

router = APIRouter(tags=["users"], prefix="/users")

@router.post('/register', response_model=User)
async def register_user(user: UserCreate):
    return await register()

@router.post('/login', response_model=User)
async def login_user(user: UserBase):
    return await login()

@router.get("/unauthenticated", response_model=str)
async def unauthenticated_path():
    return "Unauthenticated"

@router.get("/", response_model=User)
async def authenticated(username = Depends(auth_handler.auth_wrapper))
    return