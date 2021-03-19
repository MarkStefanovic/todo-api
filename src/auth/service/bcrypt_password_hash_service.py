import pydantic
from passlib import context as passlib_context

from src.auth import domain

__all__ = ("BcryptPasswordHashService",)


class BcryptPasswordHashService(domain.PasswordHashService):
    def __init__(self) -> None:
        self._context = passlib_context.CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create(self, /, plain_password: pydantic.SecretStr) -> str:
        return self._context.hash(plain_password.get_secret_value())

    def verify(self, *, hashed_password: str, plain_password: pydantic.SecretStr) -> bool:
        return self._context.verify(plain_password.get_secret_value(), hashed_password)
