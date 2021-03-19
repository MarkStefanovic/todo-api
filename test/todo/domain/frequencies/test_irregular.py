import datetime

from src import todo, core


def test_calculate_presidents_day() -> None:
    presidents_day = todo.Irregular(
        user_id=1,
        todo_id=-1,
        advance_days=30,
        category=core.TodoCategory.Reminder,
        date_added=datetime.date(1970, 1, 1),
        date_completed=None,
        description="Presidents' Day",
        note="",
        start_date=datetime.date(1900, 1, 1),
        month=todo.Month.February,
        week_day=todo.Weekday.Monday,
        week_number=3,
    )
    assert presidents_day.current_date(datetime.date(2021, 2, 1)) == datetime.date(
        2021, 2, 15
    )
