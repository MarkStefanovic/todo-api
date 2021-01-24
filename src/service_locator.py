import datetime
import functools

import sqlalchemy as sa
from sqlalchemy import orm

from src import core

__all__ = ("ServiceLocator", "services")


class ServiceLocator:
    @functools.cached_property
    def _config(self) -> core.domain.Config:
        return core.adapter.EnvironConfig()

    @functools.cached_property
    def _session_factory(self) -> orm.sessionmaker:
        engine = sa.create_engine(
            self._config.db_url, isolation_level="REPEATABLE READ"
        )
        core.adapter.db_schema.Base.metadata.create_all(bind=engine)
        return orm.sessionmaker(bind=engine)

    @functools.cached_property
    def jwt_adapter(self) -> core.domain.TokenAdapter:
        expires_delta = datetime.timedelta(
            minutes=int(self._config.access_token_expire_minutes)
        )
        return core.adapter.JwtAdapter(
            secret_key=self._config.secret_key,
            expires_delta=expires_delta,
            algorithm=self._config.hashing_algorithm,
        )

    @functools.cached_property
    def password_hasher(self) -> core.domain.PasswordHash:
        return core.adapter.BcryptPasswordHash()

    @functools.cached_property
    def user_service(self) -> core.domain.UserService:
        return core.service.SqlalchemyUserService(self._session_factory)


services = ServiceLocator()
