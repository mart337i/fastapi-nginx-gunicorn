
from typing import Annotated
from jose import jwt

class Token:
    salt: str = "djawdælwadl"
    __algorithm: str = "HS256"

    @classmethod
    def encode_token(cls, data: dict) -> str:
        return jwt.encode(data, cls.salt, algorithm=cls.__algorithm)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token, cls.salt, algorithms=[cls.__algorithm])
