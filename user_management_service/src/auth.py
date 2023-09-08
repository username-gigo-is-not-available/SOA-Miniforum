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
KEY_IDENTIFIER = environment_variables_dict["KEY_IDENTIFIER"]
CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO:
# HEADER
# {
#   "alg": "HS256",
#   "typ": "JWT",
#   "kid" : "CYDqzeQ0427MfZQ7wABuYSXPxBkQpgWh"
# }

# PAYLOAD
# {
#   "sub": "1234567890",
#   "name": "John Doe",
#   "iat": 1516239022,
#   "exp" : 1916239022
# }

# HMACSHA256(
#     base64UrlEncode(header) + "." +
#     base64UrlEncode(payload),
#
#     orYGrUbXyQ1VBFPRwnlDwakS18gOQNZI
#
# )
def hash_password(password: str) -> str:
    return CONTEXT.hash(password)


def verify_password(plain_text_password, hashed_password) -> bool:
    return CONTEXT.verify(plain_text_password, hashed_password)


def encode_access_token(data: dict) -> str:
    logger.info(f"Encoding data: {data}")
    payload = {
        "exp": (
                datetime.utcnow() + timedelta(minutes=int(environment_variables_dict["EXPIRATION_TIME"])))
        .timestamp(),
        "iat": datetime.now().timestamp(),
        "sub": data
    }
    logger.info(f"Successfully encoded jwt token with payload: {payload}")
    return jwt.encode(
        payload=payload,
        key=SECRET,
        algorithm=ALGORITHM,
        headers={"kid": KEY_IDENTIFIER}
    )


def decode_access_token(token: str) -> User:
    logger.info(f"Decoding token: {token}")
    try:
        payload = jwt.decode(jwt=token, key=SECRET, algorithms=[ALGORITHM])
        logger.info(f"Successfully decoded jwt token with payload: {payload} ")
        return User(**payload['sub'])
    except jwt.ExpiredSignatureError:
        logger.exception("Signature has expired")
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError:
        logger.exception("Invalid token")
        raise HTTPException(status_code=401, detail='Invalid token')


async def authenticate_user(user: UserLogin, db: Redis) -> User:
    registered_user = await find_user_by_email(email=user.email, db=db)
    if registered_user is not None and verify_password(user.password, registered_user.hashed_password):
        logger.info(f"Successfully authenticated user: {registered_user}")
        return registered_user
    else:
        logger.exception(invalid_credentials_message())
        raise HTTPException(status_code=401, detail=invalid_credentials_message())


async def login(form_data: OAuth2PasswordRequestForm, db: Redis) -> dict:
    user = await authenticate_user(user=UserLogin(email=form_data.username, password=form_data.password), db=db)
    if user:
        token = encode_access_token(data=user.dict())
        logger.info(f"Successfully logged in user: {user}, token: {token}")
        return {"access_token": token, "token_type": "bearer"}

    else:
        logger.exception(invalid_credentials_message())
        raise HTTPException(status_code=400, detail=invalid_credentials_message())
