import datetime

import pytest

from src import todo, core


@pytest.mark.parametrize(
    "weekday,today,expected,description",
    [
        (
            todo.Weekday.Monday,
            datetime.date(2020, 11, 16),
            datetime.date(2020, 11, 16),
            "On Monday a Monday todo should return today.",
        ),
        (
            todo.Weekday.Tuesday,
            datetime.date(2020, 11, 16),
            datetime.date(2020, 11, 10),
            "On Monday, a Tuesday todo with no advance notice should return the previous Tuesday.",
        ),
        (
            todo.Weekday.Sunday,
            datetime.date(2020, 11, 16),
            datetime.date(2020, 11, 15),
            "On Monday, a Sunday todo with no advance notice should return the previous Sunday.",
        ),
    ],
)
def test_weekday(
    weekday: todo.Weekday,
    today: datetime.date,
    expected: datetime.date,
    description: str,
) -> None:
    wk = todo.Weekly(
        advance_days=0,
        category=core.TodoCategory.Todo,
        date_added=datetime.date(2010, 1, 1),
        date_completed=None,
        description="test",
        note="",
        start_date=datetime.date(2010, 1, 1),
        todo_id=1,
        user_id=1,
        week_day=weekday,
    )
    actual = wk.current_date(today=today)
    assert actual == expected, description
