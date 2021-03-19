from __future__ import annotations

import calendar
import datetime
import typing

from src.todo.domain import todo

__all__ = ("Monthly",)


class Monthly(todo.Todo):
    month_day: int

    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        if today is None:
            today = datetime.date.today()

        cm_days = calendar.monthrange(today.year, today.month)[1]
        next_month = today + datetime.timedelta(days=cm_days - today.day + 1)
        dt1 = datetime.date(year=today.year, month=today.month, day=self.month_day)
        dt2 = datetime.date(
            year=next_month.year, month=next_month.month, day=self.month_day
        )
        if today > dt2 - datetime.timedelta(days=self.advance_days):
            return dt2
        else:
            return dt1

    def __str__(self) -> str:
        return f"Monthly, day {self.month_day}"
