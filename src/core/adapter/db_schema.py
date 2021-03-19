from __future__ import annotations

import typing

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from src.core import domain

__all__ = (
    "Base",
    "TodoDTO",
    "UserDTO",
)


Base = declarative_base()


class TodoDTO(Base):
    __tablename__ = "todo"
    __table_args__ = {"schema": "todo"}

    todo_id = sa.Column(sa.Integer, sa.Sequence("todo_id_seq"), primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("auth.user.user_id"))
    advance_days = sa.Column(sa.Integer, nullable=False)
    date_added = sa.Column(sa.Date, nullable=False)
    date_completed = sa.Column(sa.Date, nullable=True)
    days = sa.Column(sa.Integer, nullable=True)
    description = sa.Column(sa.Text, nullable=False)
    month = sa.Column(sa.Integer, nullable=True)
    month_day = sa.Column(sa.Integer, nullable=True)
    note = sa.Column(sa.Text, nullable=False)
    start_date = sa.Column(sa.Date, nullable=True)
    category = sa.Column(sa.Enum(domain.TodoCategory), nullable=False)
    week_day = sa.Column(sa.Integer, nullable=True)
    week_number = sa.Column(sa.Integer, nullable=True)
    year = sa.Column(sa.Integer, nullable=True)
    frequency = sa.Column(sa.Enum(domain.FrequencyDbName), nullable=False)

    # user = orm.relationship(UserDTO, back_populates="todos")

    def __str__(self) -> str:
        return f"TodoDTO: {self.description}"

    def __repr__(self) -> str:
        return (
            f"TodoDTO(todo_id={self.todo_id}, user_id={self.user_id}, advance_days={self.advance_days}, "
            f"date_added={self.date_added!r}, date_completed={self.date_completed!r}, days={self.days}, "
            f"description={self.description!r}, mont={self.month}, mont_day={self.month_day}, note={self.note!r}, "
            f"start_date={self.start_date!r}, category={self.start_date!r}, week_day={self.week_day!r}, "
            f"week_number={self.week_number}, year={self.year}, frequency={self.frequency!r})"
        )


class UserDTO(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "auth"}

    user_id = sa.Column(sa.Integer, sa.Sequence("user_id_seq"), primary_key=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    password_hash = sa.Column(sa.String, nullable=False)

    todos = orm.relationship(TodoDTO)
    # todos = orm.relationship("TodoDTO", back_populates="user")
    # we don't bother with cascade options since it doesn't work with sqlite

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, username={self.username!r}, password_hash={self.password_hash!r})"

    def __str__(self) -> str:
        return f"UserDTO: {self.username}"


def to_dict(obj) -> typing.Dict[str, typing.Any]:  # type: ignore
    return {key: attr.value for key, attr in sorted(sa.inspect(obj).attrs.items())}
