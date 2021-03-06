from __future__ import annotations

import datetime
import functools
import typing

from src.todo.domain import todo

__all__ = ("Easter",)


class Easter(todo.Todo):
    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        if today is None:
            today = datetime.date.today()
        assert self.advance_days < 365
        cy = calculate_easter(today.year)
        ny = calculate_easter(today.year + 1)
        if today >= ny - datetime.timedelta(days=self.advance_days):
            return ny
        else:
            return cy

    def __str__(self) -> str:
        return "Easter"


@functools.lru_cache()
def calculate_easter(year: int, /) -> datetime.date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = ((19 * a) + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + (2 * e) + (2 * i) - h - k) % 7
    m = (a + (11 * h) + (22 * l)) // 451
    month = (h + l - (7 * m) + 114) // 31
    day = ((h + l - (7 * m) + 114) % 31) + 1
    return datetime.date(year, month, day)
