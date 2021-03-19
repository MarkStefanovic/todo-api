import typing

import pydantic
from sqlalchemy import orm

from src import core
from src.auth import domain

__all__ = ("SqlalchemyUserRepository",)


class SqlalchemyUserRepository(domain.UserRepo):
    def __init__(self, /, session: orm.Session):
        self._session = session

    def add_user(self, *, username: str, email: pydantic.EmailStr, password_hash: str) -> domain.User:
        dto = core.UserDTO(username=username, email=email, password_hash=password_hash)
        self._session.add(dto)
        self._session.flush()
        return user_dto_to_domain(dto)

    def get_user(self, /, username: str) -> typing.Optional[domain.User]:
        if dto := self._session.query(core.UserDTO).filter_by(username=username).first():
            return user_dto_to_domain(dto)
        return None

    def remove_user(self, /, username: str) -> None:
        user_dto: typing.Optional[core.UserDTO] = self._session.query(core.UserDTO).filter_by(username=username).first()
        if user_dto:
            self._session.query(core.TodoDTO).filter_by(user_id=user_dto.user_id).delete()
            self._session.query(core.UserDTO).filter_by(user_id=user_dto.user_id).delete()


def user_dto_to_domain(dto: core.UserDTO, /) -> domain.User:
    return domain.User(
        user_id=dto.user_id,
        username=dto.username,
        email=pydantic.EmailStr(dto.email),
        password_hash=dto.password_hash,
    )


# def user_to_user_dto(user: domain.User, /) -> core.UserDTO:
#     email = pydantic.EmailStr(user.email)
#     if user.user_id == -1:
#         return core.UserDTO(
#             username=user.username,
#             email=email,
#             password_hash=user.password_hash,
#         )
#     else:
#         return core.UserDTO(
#             user_id=user.user_id,
#             username=user.username,
#             email=email,
#             password_hash=user.password_hash,
#         )
