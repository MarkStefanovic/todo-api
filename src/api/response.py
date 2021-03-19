from __future__ import annotations

import datetime
import typing

import pydantic

from src import core, todo, auth

__all__ = (
    "TodoResponse",
    "UserResponse",
)


class TodoResponse(pydantic.BaseModel):
    todo_id: int
    category: core.TodoCategory
    description: str
    frequency: str
    next: datetime.date
    display: bool
    note: str

    class Config:
        allow_mutation = False
        anystr_strip_whitespace = True

    @staticmethod
    def from_domain(
        domain: todo.Todo, /, *, today: typing.Optional[datetime.date] = None
    ) -> TodoResponse:
        if today is None:
            today = datetime.date.today()
        return TodoResponse(
            todo_id=domain.todo_id,
            category=domain.category,
            description=domain.description,
            frequency=str(domain),
            next=domain.current_date(today),
            display=domain.display(today),
            note=domain.note,
        )


class UserResponse(pydantic.BaseModel):
    username: str
    email: str

    @staticmethod
    def from_domain(domain: auth.User) -> UserResponse:
        return UserResponse(
            username=domain.username,
            email=domain.email,
        )
