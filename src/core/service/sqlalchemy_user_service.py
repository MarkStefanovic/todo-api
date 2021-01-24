import typing

import pydantic
from sqlalchemy import orm

from src.core import adapter, domain

__all__ = ("SqlalchemyUserService",)


class SqlalchemyUserService(domain.UserService):
    def __init__(self, /, session_factory: orm.sessionmaker):
        self._session_factory = session_factory

    def create_user(
        self,
        *,
        username: str,
        email: pydantic.EmailStr,
        password_hash: str,
    ) -> domain.User:
        with adapter.SqlAlchemyUnitOfWork(self._session_factory) as uow:
            uow.user_repository.add_user(
                username=username, email=email, password_hash=password_hash
            )
            uow.commit()
            return self.get_user(username)

    def get_user(self, /, username: str) -> typing.Optional[domain.User]:
        with adapter.SqlAlchemyUnitOfWork(self._session_factory) as uow:
            maybe_user = uow.user_repository.get_user(username)
            if maybe_user is None:
                raise domain.exception.CredentialsException("User not found")
            if maybe_user.active:
                return maybe_user
            else:
                raise domain.exception.InactiveUserException()

    def retire_user(self, /, username: str) -> None:
        with adapter.SqlAlchemyUnitOfWork(self._session_factory) as uow:
            uow.user_repository.retire_user(username)
