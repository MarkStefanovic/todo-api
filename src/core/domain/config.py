import abc
import typing

import pydantic

from starlette.datastructures import URL, Secret


__all__ = ("Config",)

#  To generate a secret_key run the following command: openssl rand -hex 32


# class Config(pydantic.BaseSettings):
#     db_url: pydantic.AnyUrl
#     secret_key: pydantic.SecretStr
#     access_token_expire_minutes: pydantic.PositiveInt = pydantic.PositiveInt(30)
#     hashing_algorithm: pydantic.constr(strip_whitespace=True) = "HS256"  # type: ignore
#
#     def __repr__(self) -> str:
#         return (
#             f"{self.__class__.__qualname__}(db_url=pydantic.SecretStr(...), secret_key=pydantic.SecretKey(...), "
#             f"access_token_expire_minutes={self.access_token_expire_minutes!r}, "
#             f"hashing_algorithm={self.hashing_algorithm!r})"
#         )
#
#     __str__ = __repr__


class Config(abc.ABC):
    @property
    @abc.abstractmethod
    def allowed_hosts(self) -> typing.List[str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def debug(self) -> bool:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def db_url(self) -> URL:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def secret_key(self) -> Secret:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def access_token_expire_minutes(self) -> int:
        raise NotImplementedError

    @property
    def hashing_algorithm(self) -> str:
        return "HS256"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(db_url=pydantic.SecretStr(...), secret_key=pydantic.SecretKey(...), "
            f"access_token_expire_minutes={self.access_token_expire_minutes!r}, "
            f"hashing_algorithm={self.hashing_algorithm!r})"
        )

    __str__ = __repr__
