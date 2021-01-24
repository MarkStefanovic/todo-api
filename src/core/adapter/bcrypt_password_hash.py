import pydantic
from passlib import context as passlib_context

from src.core import domain

__all__ = ("BcryptPasswordHash",)


class BcryptPasswordHash(domain.PasswordHash):
    def __init__(self):
        self._context = passlib_context.CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create(self, /, plain_password: pydantic.SecretStr) -> str:
        return self._context.hash(plain_password.get_secret_value())

    def verify(self, *, hashed_password: str, plain_password: pydantic.SecretStr) -> bool:
        return self._context.verify(plain_password.get_secret_value(), hashed_password)
