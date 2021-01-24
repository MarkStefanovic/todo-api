import abc
import typing

import pydantic

from src.core.domain import user as domain_user


__all__ = ("UserRepo",)


class UserRepo(abc.ABC):
    @abc.abstractmethod
    def add_user(
        self, *, username: str, email: pydantic.EmailStr, password_hash: str
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, /, username: str) -> typing.Optional[domain_user.User]:
        raise NotImplementedError

    @abc.abstractmethod
    def retire_user(self, /, username: str) -> None:
        raise NotImplementedError
