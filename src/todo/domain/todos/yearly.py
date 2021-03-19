from __future__ import annotations

import datetime
import typing

from src.todo.domain import month, todo

__all__ = ("Yearly",)


class Yearly(todo.Todo):
    day: int
    month: month.Month

    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        if today is None:
            today = datetime.date.today()
        dt1 = datetime.date(year=today.year, month=self.month, day=self.day)
        dt2 = datetime.date(year=today.year + 1, month=self.month, day=self.day)
        if today > dt2 - datetime.timedelta(days=self.advance_days):
            return dt2
        else:
            return dt1

    def __str__(self) -> str:
        return f"{self.month!s} {self.day}"
