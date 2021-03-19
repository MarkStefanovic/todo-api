from __future__ import annotations

import datetime
import typing

from src import core
from src.todo.domain import todo

__all__ = ("Once",)


class Once(todo.Todo):
    once_date: datetime.date

    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        return self.once_date

    @staticmethod
    def db_name() -> typing.Literal[core.FrequencyDbName.ONCE]:
        return core.FrequencyDbName.ONCE

    def __str__(self) -> str:
        return self.once_date.strftime("%Y-%m-%d")
