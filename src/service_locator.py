import abc
import datetime
import functools

import sqlalchemy as sa
from sqlalchemy import orm

from src import auth, todo, core

__all__ = ("ServiceLocator", "default")


class ServiceLocator:
    @abc.abstractmethod
    def password_hasher(self) -> auth.PasswordHashService:
        raise NotImplementedError

    @abc.abstractmethod
    def todo_service(self) -> todo.SqlAlchemyTodoService:
        raise NotImplementedError

    @abc.abstractmethod
    def token_service(self) -> auth.TokenService:
        raise NotImplementedError

    @abc.abstractmethod
    def user_service(self) -> auth.UserService:
        raise NotImplementedError


class SqlAlchemyServiceLocator(ServiceLocator):
    def __init__(self, /, config: core.Config):
        self._config = config

    def token_service(self) -> auth.TokenService:
        expires_delta = datetime.timedelta(
            minutes=int(self._config.access_token_expire_minutes)
        )
        return auth.JwtTokenService(
            secret_key=self._config.secret_key,
            expires_delta=expires_delta,
            algorithm=self._config.hashing_algorithm,
        )

    def password_hasher(self) -> auth.PasswordHashService:
        return auth.BcryptPasswordHashService()

    def todo_service(self) -> todo.SqlAlchemyTodoService:
        return todo.SqlAlchemyTodoService(self._uow)

    def user_service(self) -> auth.UserService:
        return auth.SqlalchemyUserService(self._uow)

    @functools.cached_property
    def _uow(self) -> core.SqlAlchemyUnitOfWork:
        engine = sa.create_engine(
            str(self._config.db_url), isolation_level="REPEATABLE READ"
        )
        core.adapter.db_schema.Base.metadata.create_all(bind=engine)
        session_factory = orm.sessionmaker(bind=engine)
        return core.SqlAlchemyUnitOfWork(session_factory)


@functools.lru_cache()
def default() -> ServiceLocator:
    return SqlAlchemyServiceLocator(core.EnvironConfig())
