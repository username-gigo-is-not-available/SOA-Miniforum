import jwt
from fastapi import HTTPException
from fastapi.logger import logger
from passlib.context import CryptContext

from src.settings import environment_variables_dict

SECRET = environment_variables_dict["SECRET"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(environment_variables_dict["EXPIRATION_TIME"])
ALGORITHM = environment_variables_dict["ALGORITHM"]
KEY_IDENTIFIER = environment_variables_dict["KEY_IDENTIFIER"]
CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_access_token(token: str) -> dict:
    logger.info(f"Decoding token: {token}")
    try:
        payload = jwt.decode(jwt=token, key=SECRET, algorithms=[ALGORITHM])
        logger.info(f"Successfully decoded jwt token with payload: {payload} ")
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        logger.exception("Signature has expired")
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.InvalidTokenError:
        logger.exception("Invalid token")
        raise HTTPException(status_code=401, detail='Invalid token')
