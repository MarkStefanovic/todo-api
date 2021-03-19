from __future__ import annotations

import datetime
import typing

from src.todo.domain import todo

__all__ = ("XDays",)


class XDays(todo.Todo):
    start_date: datetime.date
    days: int

    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        if today is None:
            today = datetime.date.today()

        days_since_start = (today - self.start_date).days
        days_since_last = days_since_start % self.days
        prior_date = today - datetime.timedelta(days=days_since_last)
        return prior_date + datetime.timedelta(days=self.days)

    def __str__(self) -> str:
        return f"Every {self.days} days"
