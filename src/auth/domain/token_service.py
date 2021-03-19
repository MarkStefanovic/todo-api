import abc
import typing

from src.auth import domain

__all__ = ("TokenService",)


class TokenService(abc.ABC):
    @abc.abstractmethod
    def create(self, /, data: typing.Dict[str, typing.Any]) -> domain.Token:
        raise NotImplementedError

    @abc.abstractmethod
    def username(self, /, token: str) -> str:
        raise NotImplementedError
