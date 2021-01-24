import abc

from pydantic import typing

from src.core.domain import token as token_model

__all__ = ("TokenAdapter",)


class TokenAdapter(abc.ABC):
    @abc.abstractmethod
    def create(self, /, data: typing.Dict[str, typing.Any]) -> token_model.Token:
        raise NotImplementedError

    @abc.abstractmethod
    def username(self, /, token: str) -> str:
        raise NotImplementedError
