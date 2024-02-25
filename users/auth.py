from datetime import datetime, timedelta

from jose import jwt
from passlib.hash import pbkdf2_sha256

from app.config import Settings
from app.users.dao import UserDAO
from app.users.models import User


settings = Settings()


def create_access_token(data: dict, expired_day: int = 1):
    to_encode = data.copy()
    now: datetime = datetime.utcnow()
    expired_date: datetime = now + timedelta(days=expired_day)
    to_encode.update(exp=expired_date.timestamp(), iat=now.timestamp())
    return jwt.encode(
        claims=to_encode,
        key=settings.security.private_key.read_text(),
        algorithm=settings.security.algorith,
    )


async def authenticate_user(username: str, password: str):
    user: User = await UserDAO.get_username_and_pass(username)
    if user and pbkdf2_sha256.verify(password, user.password):
        return user
    return None
