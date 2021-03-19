from __future__ import annotations

import abc
import datetime
import typing

import pydantic

from src import core

__all__ = ("Todo",)


class Todo(pydantic.BaseModel, abc.ABC):
    advance_days: int
    category: core.TodoCategory
    date_added: datetime.date
    date_completed: typing.Optional[datetime.date]
    description: str
    note: str
    start_date: typing.Optional[datetime.date]
    todo_id: int
    user_id: int

    class Config:
        allow_mutation = False
        anystr_strip_whitespace = True

    def display(self, /, today: typing.Optional[datetime.date] = None) -> bool:
        if today is None:
            today = datetime.date.today()
        current_date = self.current_date(today)
        current_advance_date = current_date - datetime.timedelta(days=self.advance_days)
        if self.date_completed and self.date_completed >= current_advance_date:  # noqa
            return False
        elif today >= current_advance_date:
            return True
        else:
            return False

    @abc.abstractmethod
    def current_date(
        self, /, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        raise NotImplementedError

    def days_until(self, /, today: typing.Optional[datetime.date] = None) -> int:
        if today is None:
            today = datetime.date.today()
        return (self.current_date(today) - today).days
