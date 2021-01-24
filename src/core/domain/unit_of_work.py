from __future__ import annotations
import abc
import types
import typing

from src.core import domain


__all__ = ("UnitOfWork",)


class UnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self) -> UnitOfWork:
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> typing.Literal[False]:
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def user_repository(self) -> domain.UserRepo:
        raise NotImplementedError
