from __future__ import annotations

import datetime
import typing

from src.todo.domain import weekday, todo

__all__ = ("Weekly",)


class Weekly(todo.Todo):
    week_day: weekday.Weekday

    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        if today is None:
            today = datetime.date.today()

        weekday_diff = weekday.Weekday.from_date(today).value - self.week_day.value
        if weekday_diff == 0:
            next_date = today
        elif weekday_diff < 0:
            next_date = today - datetime.timedelta(days=weekday_diff)
        else:
            next_date = today + datetime.timedelta(days=7 - weekday_diff)

        if today >= next_date - datetime.timedelta(days=self.advance_days):
            return next_date
        else:
            return next_date - datetime.timedelta(days=7)

    def __str__(self) -> str:
        return self.week_day.short_name
