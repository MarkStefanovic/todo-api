from __future__ import annotations

import datetime
import typing

from src.todo.domain import todo

__all__ = ("Daily",)


class Daily(todo.Todo):
    advance_days: int = 0

    def current_date(
        self, /, today: typing.Optional[datetime.date] = None
    ) -> datetime.date:
        if today is None:
            today = datetime.date.today()
        return today

    def __repr__(self) -> str:
        return f"Daily()"

    def __str__(self) -> str:
        return "Daily"
