import abc

import pydantic

from src.auth import domain

__all__ = ("UserService",)


class UserService(abc.ABC):
    @abc.abstractmethod
    def create_user(
        self, *, username: str, email: pydantic.EmailStr, password_hash: str
    ) -> domain.User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, /, username: str) -> domain.User:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_user(self, username: str) -> None:
        raise NotImplementedError
