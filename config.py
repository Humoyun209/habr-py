from environs import Env
from pathlib import Path

from pydantic import BaseModel


BASE_DIR = Path(__file__).parent
env_path = Path(Path(__file__).parent.parent / ".env")


def get_env():
    env = Env()
    env.read_env(env_path)
    return env


class AuthJWT(BaseModel):
    public_key: Path = Path(BASE_DIR / "users/certs/jwt-public.pem")
    private_key: Path = Path(BASE_DIR / "users/certs/jwt-private.pem")
    algorithm: str = "RS256"
    expired_time: int = 5


class DBSettings(BaseModel):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str


def get_settings() -> DBSettings:
    env = get_env()
    return DBSettings(
        DB_NAME=env.str("DB_NAME"),
        DB_HOST=env.str("DB_HOST"),
        DB_PORT=env.int("DB_PORT"),
        DB_USER=env.str("DB_USER"),
        DB_PASS=env.str("DB_PASS"),
    )


class Settings(BaseModel):
    db: DBSettings = get_settings()
    security: AuthJWT = AuthJWT()
