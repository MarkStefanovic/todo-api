import abc
import typing

import pydantic

from src.auth import domain
from src.auth.domain import user

__all__ = ("UserRepo",)


class UserRepo(abc.ABC):
    @abc.abstractmethod
    def add_user(
        self, *, username: str, email: pydantic.EmailStr, password_hash: str
    ) -> user.User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, /, username: str) -> typing.Optional[domain.User]:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_user(self, /, username: str) -> None:
        raise NotImplementedError
