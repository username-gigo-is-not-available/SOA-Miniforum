from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from redis.asyncio import Redis

from src.auth import login, decode_access_token
from src.crud import create, get, update, delete, query
from src.database import get_db
from src.database_models import User
from src.schemas import UserCreate, UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter(tags=["users"], prefix="/users")


@router.post('/register', response_model=User)
async def register_user(user: UserCreate, db: Redis = Depends(get_db)):
    return await create(user=user, db=db)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Redis = Depends(get_db)):
    return await get(user_id=user_id, db=db)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Redis = Depends(get_db)):
    return await update(user_id=user_id, user=user, db=db)


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int, db: Redis = Depends(get_db)):
    return await delete(user_id=user_id, db=db)


@router.post("/search", response_model=list[User])
async def list_users(email_pattern: str, db: Redis = Depends(get_db)):
    return await query(email_pattern=email_pattern, db=db)


@router.post("/login", response_model=str)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Redis = Depends(get_db)):
    return await login(form_data=form_data, db=db)


@router.get("/authenticated", response_model=User)
async def authenticated_user(token: str = Depends(oauth2_scheme)):
    return await decode_access_token(token=token)
