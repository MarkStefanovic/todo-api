import pydantic

from src.core import domain

__all__ = ("EnvironConfig",)


class EnvironConfig(domain.Config):
    db_url: pydantic.PostgresDsn
    access_token_expire_minutes: pydantic.PositiveInt = 30
    hashing_algorithm: pydantic.constr(strip_whitespace=True) = "HS256"  # type: ignore

    class Config:
        allow_mutation = False

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(...)"
