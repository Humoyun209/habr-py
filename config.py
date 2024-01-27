from dataclasses import dataclass
from environs import Env


@dataclass
class DBSettings:
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str


@dataclass
class Secret:
    PUBLIC_KEY: str
    ALGORITHM: str


def get_secret(path_env: str = None):
    env = Env()
    env.read_env(path_env)
    return Secret(
        PUBLIC_KEY=env.str('PUBLIC_KEY'),
        ALGORITHM=env.str('ALGORITHM')
    )


def get_settings(path_env: str = None):
    env = Env()
    env.read_env(path_env)
    return DBSettings(
        DB_NAME=env.str('DB_NAME'),
        DB_HOST=env.str('DB_HOST'),
        DB_PORT=env.int('DB_PORT'),
        DB_USER=env.str('DB_USER'),
        DB_PASS=env.str('DB_PASS')
    )