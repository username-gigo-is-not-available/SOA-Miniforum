from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext


class AuthHandler:
    security = HTTPBearer()
    context = CryptContext(schemes=['bcr'])
    secret = ...

    def get_password_hash(self, password):
        return self.context.hash(password)

    def verify_password(self, plain_text_password, hashed_password):
        return self.context.verify(plain_text_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'expiration_time': datetime.utcnow() + timedelta(minutes=...),
            'issued_at_time': datetime.now(),
            "subject": user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=...
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=...)
            return payload['subject']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
