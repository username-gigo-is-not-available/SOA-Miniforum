from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from redis.asyncio import Redis
from starlette.responses import RedirectResponse

from src.auth import login, decode_access_token
from src.crud import create, get, update, delete, query, redirect_to_gateway
from src.database import get_cache
from src.database_models import User
from src.schemas import UserCreate, UserUpdate
from src.settings import environment_variables_dict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=environment_variables_dict["TOKEN_URL"])

router = APIRouter(tags=["users"], prefix="/users")


@router.post('/register/', response_model=User)
async def register_user(user: UserCreate, cache: Redis = Depends(get_cache)):
    return await create(user=user, cache=cache)


@router.get("/{user_id}/", response_model=User)
async def get_user(user_id: int, cache: Redis = Depends(get_cache)):
    return await get(user_id=user_id, cache=cache)


@router.put("/{user_id}/", response_model=User)
async def update_user(user_id: int, user: UserUpdate, cache: Redis = Depends(get_cache)):
    return await update(user_id=user_id, user_update=user, cache=cache)


@router.delete("/{user_id}/", response_model=User)
async def delete_user(user_id: int, cache: Redis = Depends(get_cache)):
    return await delete(user_id=user_id, cache=cache)


@router.post("/search/", response_model=list[User])
async def list_users(email_pattern: str = ".*", cache: Redis = Depends(get_cache)):
    return await query(email_pattern=email_pattern, cache=cache)


@router.post("/login/", response_model=dict)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), cache: Redis = Depends(get_cache)):
    return await login(form_data=form_data, db=cache)


@router.get("/authenticated", response_model=User)
async def authenticated_user(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token=token)


@router.get("/redirect", response_class=RedirectResponse, status_code=302)
async def redirect(token: str = Depends(oauth2_scheme)):
    return redirect_to_gateway(token=token)
