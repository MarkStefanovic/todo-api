import typing

from starlette.config import Config
from starlette.datastructures import Secret, URL, CommaSeparatedStrings

from src.core import domain

__all__ = ("EnvironConfig",)


class EnvironConfig(domain.Config):
    def __init__(self) -> None:
        self._config = Config(".env")

    @property
    def allowed_hosts(self) -> typing.List[str]:
        return self._config(
            "ALLOWED_HOSTS",
            cast=CommaSeparatedStrings,
            default="",
        )

    @property
    def debug(self) -> bool:
        return self._config("DEBUG", cast=bool, default=False)

    @property
    def db_url(self) -> URL:
        return self._config("DB_URL", cast=URL)

    @property
    def secret_key(self) -> Secret:
        return self._config("SECRET_KEY", cast=Secret)

    @property
    def access_token_expire_minutes(self) -> int:
        return self._config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=120)
