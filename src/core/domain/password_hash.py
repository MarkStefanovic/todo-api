from __future__ import annotations

import abc

import pydantic

__all__ = ("PasswordHash",)


class PasswordHash(abc.ABC):
    @abc.abstractmethod
    def create(self, /, plain_password: pydantic.SecretStr) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def verify(self, *, hashed_password: str, plain_password: pydantic.SecretStr) -> bool:
        raise NotImplementedError
