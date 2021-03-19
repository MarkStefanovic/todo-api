import types
import typing

from sqlalchemy import orm

from src.core import domain

__all__ = ("SqlAlchemyUnitOfWork",)


class SqlAlchemyUnitOfWork(domain.UnitOfWork):
    def __init__(self, /, session_factory: orm.sessionmaker):
        self._session_factory = session_factory

    def __enter__(self) -> domain.UnitOfWork:
        self._session = self._session_factory()
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> typing.Literal[False]:
        self.session.rollback()
        self.session.close()
        return False

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    @property
    def session(self) -> orm.Session:
        assert self._session is not None
        return self._session
