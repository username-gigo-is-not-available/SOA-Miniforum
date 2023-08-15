from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm

from src.crud import *
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from src.schemas import UserLogin
from src.settings import environment_variables_dict
from src.exceptions import invalid_credentials_message

SECRET = environment_variables_dict["SECRET"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(environment_variables_dict["EXPIRATION_TIME"])
ALGORITHM = environment_variables_dict["ALGORITHM"]
CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return CONTEXT.hash(password)


def verify_password(plain_text_password, hashed_password):
    return CONTEXT.verify(plain_text_password, hashed_password)


def encode_access_token(data: dict) -> str:
    payload = {
        "expiration_time": (
                datetime.utcnow() + timedelta(minutes=int(environment_variables_dict["EXPIRATION_TIME"])))
        .strftime("%Y-%m-%d %H:%M:%S"),
        "issued_at_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "subject": data
    }
    return jwt.encode(
        payload=payload,
        key=SECRET,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])
        return payload['data']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


async def authenticate_user(user: UserLogin, db: Redis):
    registered_user = await find_user_by_email(email=user.email, db=db)
    if registered_user is not None and verify_password(user.password, registered_user.hashed_password):
        return registered_user
    else:
        raise HTTPException(status_code=401, detail=invalid_credentials_message())


async def login(form_data: OAuth2PasswordRequestForm, db: Redis) -> str:
    user = await authenticate_user(user=UserLogin(email=form_data.username, password=form_data.password), db=db)
    if user:
        return encode_access_token(data={"user_id": user.id})
    else:
        raise HTTPException(status_code=400, detail=invalid_credentials_message())


