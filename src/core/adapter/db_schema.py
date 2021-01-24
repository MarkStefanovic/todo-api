from __future__ import annotations

import pydantic
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from src.core import domain

__all__ = ("UserDTO",)


Base = declarative_base()


class UserDTO(Base):  # type: ignore
    __tablename__ = "user"

    id = sa.Column(sa.Integer, sa.Sequence("user_id_seq"), primary_key=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    active = sa.Column(sa.Boolean, nullable=False)
    password_hash = sa.Column(sa.String, nullable=False)

    @staticmethod
    def from_domain(user: domain.User) -> UserDTO:
        data = user.dict()
        if user.id == -1:
            del data["id"]
        return UserDTO(**data)

    def to_domain(self) -> domain.User:
        return domain.User(
            id=self.id,
            username=self.username,
            email=pydantic.EmailStr(self.email),
            active=self.active,
            password_hash=self.password_hash,
        )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, username={self.username!r}, active={self.active!r}, "
            f"password_hash={self.password_hash!r})"
        )
