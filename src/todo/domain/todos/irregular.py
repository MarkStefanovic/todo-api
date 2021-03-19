from __future__ import annotations

import calendar
import datetime
import functools
import itertools
import typing

from src.todo.domain import month, weekday, todo

__all__ = ("Irregular",)


class Irregular(todo.Todo):
    month: month.Month
    week_day: weekday.Weekday
    week_number: int

    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        if today is None:
            today = datetime.date.today()

        assert self.advance_days < 365
        dt1 = get_x_weekday_of_month(
            year=today.year,
            month=self.month,
            week_num=self.week_number,
            week_day=self.week_day,
        )
        dt2 = get_x_weekday_of_month(
            year=today.year + 1,
            month=self.month,
            week_num=self.week_number,
            week_day=self.week_day,
        )
        if today > dt2 - datetime.timedelta(days=self.advance_days):
            return dt2
        else:
            return dt1

    def __str__(self) -> str:
        return f"Irregular"


@functools.lru_cache()
def get_x_weekday_of_month(
    year: int, month: int, week_num: int, week_day: weekday.Weekday
) -> datetime.date:
    days_in_month = calendar.monthrange(year, month)[1]
    return list(
        itertools.islice(
            (
                dt
                for day in range(1, days_in_month, 1)
                if (dt := datetime.date(year, month, day)).weekday()
                == week_day.py_weekday
            ),
            week_num,
        )
    )[-1]
