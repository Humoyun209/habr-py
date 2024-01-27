from datetime import datetime, timedelta

from jose import jwt
from passlib.hash import pbkdf2_sha256

from app.config import get_secret
from app.users.dao import UserDAO
from app.users.models import User


def create_access_token(data: dict, expired_day: int = 1):
    to_encode = data.copy()
    expired_date = datetime.utcnow() + timedelta(days=expired_day)
    to_encode.update({'exp': expired_date.timestamp()})
    return jwt.encode(
        claims=to_encode,
        key=get_secret().PUBLIC_KEY,
        algorithm=get_secret().ALGORITHM
    )


async def authenticate_user(username: str, password: str):
    user: User = await UserDAO.get_user(username)
    if user and pbkdf2_sha256.verify(password, user.password):
        return user
    return None
