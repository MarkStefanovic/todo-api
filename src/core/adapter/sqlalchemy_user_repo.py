import typing

import pydantic
from sqlalchemy import orm

from src.core import domain
from src.core.adapter import db_schema

__all__ = ("SqlalchemyUserRepo",)


class SqlalchemyUserRepo(domain.UserRepo):
    def __init__(self, /, session: orm.Session):
        self._session = session

    def add_user(self, *, username: str, email: pydantic.EmailStr, password_hash: str) -> None:
        dto = db_schema.UserDTO(username=username, email=email, active=True, password_hash=password_hash)
        self._session.add(dto)

    def get_user(self, /, username: str) -> typing.Optional[domain.User]:
        if user_dto := self._session.query(db_schema.UserDTO).filter_by(username=username).first():
            return user_dto.to_domain()
        return None

    def retire_user(self, /, username: str) -> None:
        self._session.query(db_schema.UserDTO).filter_by(username=username).update({"active": False})
