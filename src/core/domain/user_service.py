import abc
import typing

from src.core import domain

__all__ = ("UserService",)


class UserService(abc.ABC):
    @abc.abstractmethod
    def create_user(
        self, *, username: str, email: str, password_hash: str
    ) -> domain.User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, /, username: str) -> typing.Optional[domain.User]:
        raise NotImplementedError

    @abc.abstractmethod
    def retire_user(self, username: str) -> None:
        raise NotImplementedError
