import asyncio
import datetime
import typing

import freezegun
import pydantic

from src.api.routes.todos import (
    update_todo,
    add_daily_todo,
    update_daily_todo,
    add_irregular_todo,
    update_irregular_todo,
    add_monthly_todo,
    update_monthly_todo,
    add_one_time_todo,
    update_one_time_todo,
    add_weekly_todo,
    update_weekly_todo,
    add_xdays_todo,
    update_xdays_todo,
    add_yearly_todo,
    delete_todo,
    all_todos,
)

from src import todo as todo_domain, core, api, auth


class DummyTodoService(todo_domain.TodoService):
    def __init__(self, /, todos: typing.List[todo_domain.Todo]):
        self._todos = todos

    def all(self, /, user_id: int) -> typing.List[todo_domain.Todo]:
        return self._todos

    def add_todo(self, *, user_id: int, todo: todo_domain.Todo) -> todo_domain.Todo:
        self._todos.append(todo)
        return todo

    def delete_todo(self, *, user_id: int, todo_id: int) -> None:
        self._todos = [t for t in self._todos if t.todo_id != todo_id]

    def get_by_id(
        self, *, user_id: int, todo_id: int
    ) -> typing.Optional[todo_domain.Todo]:
        return next(
            t for t in self._todos if t.user_id == user_id and t.todo_id == todo_id
        )

    def get_current_todos(
        self,
        *,
        user_id: int,
        category: str,
        today: datetime.date = datetime.date.today(),
    ) -> typing.List[todo_domain.Todo]:
        raise NotImplementedError

    def get_todos_completed_today(
        self, *, user_id: int, today: datetime.date = datetime.date.today()
    ) -> typing.List[todo_domain.Todo]:
        raise NotImplementedError

    def mark_complete(self, *, user_id: int, todo_id: int) -> None:
        raise NotImplementedError

    def update_todo(self, *, user_id: int, todo: todo_domain.Todo) -> todo_domain.Todo:
        self._todos = []
        for t in self._todos:
            if t.todo_id == todo.todo_id:
                updates = todo.dict()
                updated_todo = t.copy(update=updates)
                self._todos.append(updated_todo)
            else:
                self._todos.append(t)
        return todo


@freezegun.freeze_time("2010-01-01")
def test_update_todo_happy_path():
    todo_service = DummyTodoService(
        [
            todo_domain.Daily(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Run tests for user 1",
                note="",
                start_date=datetime.date(2009, 1, 1),
                todo_id=1,
                user_id=1,
            ),
            todo_domain.Daily(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Run tests for user 2",
                note="",
                start_date=datetime.date(2009, 1, 1),
                todo_id=2,
                user_id=2,
            ),
        ]
    )
    result = update_todo(
        user_id=1,
        todo_id=1,
        todo_service=todo_service,
        updates={"date_completed": datetime.date(2011, 2, 3)},
    )
    assert result == api.TodoResponse(
        todo_id=1,
        category=core.TodoCategory.Todo,
        description="Run tests for user 1",
        frequency="Daily",
        next=datetime.date(2010, 1, 1),
        display=False,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_add_daily_todo_happy_path() -> None:
    todo_service = DummyTodoService([])
    result = asyncio.run(
        add_daily_todo(
            description="Make bed",
            note=None,
            start_date=datetime.date(2010, 1, 1),
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=-1,
        category=core.TodoCategory.Todo,
        description="Make bed",
        frequency="Daily",
        next=datetime.date.today(),
        display=True,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_update_daily_todo_happy_path() -> None:
    todo_service = DummyTodoService(
        [
            todo_domain.Daily(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Run tests for user 1",
                note="",
                start_date=datetime.date(2009, 1, 1),
                todo_id=1,
                user_id=1,
            ),
            todo_domain.Daily(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Run tests for user 2",
                note="",
                start_date=datetime.date(2009, 1, 1),
                todo_id=2,
                user_id=2,
            ),
        ]
    )
    result = asyncio.run(
        update_daily_todo(
            todo_id=2,
            description="Make bed",
            current_user=auth.User(
                user_id=2,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=2,
        category=core.TodoCategory.Todo,
        description="Make bed",
        frequency="Daily",
        next=datetime.date.today(),
        display=True,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_add_irregular_todo_happy_path() -> None:
    todo_service = DummyTodoService([])
    result = asyncio.run(
        add_irregular_todo(
            description="Make bed",
            note=None,
            start_date=datetime.date(2010, 1, 1),
            advance_days=14,
            month=1,
            week=2,
            week_day=3,
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=-1,
        category=core.TodoCategory.Todo,
        description="Make bed",
        frequency="Irregular",
        next=datetime.date(2010, 1, 12),
        display=True,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_update_irregular_todo_happy_path() -> None:
    todo_service = DummyTodoService(
        [
            todo_domain.Irregular(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Run tests for user 1",
                note="",
                start_date=datetime.date(2009, 1, 1),
                todo_id=1,
                user_id=1,
                month=todo_domain.Month.January,
                week_day=todo_domain.Weekday.Friday,
                week_number=4,
            ),
            todo_domain.Irregular(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Run tests for user 2",
                note="",
                start_date=datetime.date(2009, 1, 1),
                todo_id=2,
                user_id=2,
                month=todo_domain.Month.October,
                week_day=todo_domain.Weekday.Thursday,
                week_number=3,
            ),
        ]
    )
    result = asyncio.run(
        update_irregular_todo(
            todo_id=2,
            description="Make bed",
            current_user=auth.User(
                user_id=2,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=2,
        category=core.TodoCategory.Todo,
        description="Make bed",
        frequency="Irregular",
        next=datetime.date(2010, 10, 21),
        display=False,
        note="",
    )


@freezegun.freeze_time("2010-10-08")
def test_add_monthly_todo_happy_path():
    todo_service = DummyTodoService([])
    result = asyncio.run(
        add_monthly_todo(
            description="Dust",
            advance_days=3,
            month_day=10,
            note=None,
            start_date=datetime.date(2010, 1, 1),
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=-1,
        category=core.TodoCategory.Todo,
        description="Dust",
        frequency="Monthly, day 10",
        next=datetime.date(2010, 10, 10),
        display=True,
        note="",
    )


@freezegun.freeze_time("2010-10-10")
def test_update_monthly_todo_happy_path():
    todo_service = DummyTodoService(
        [
            todo_domain.Yearly(
                todo_id=1,
                user_id=1,
                category=core.TodoCategory.Todo,
                description="Dust",
                advance_days=3,
                month=todo_domain.Month(10),
                day=10,
                note="",
                start_date=datetime.date(2010, 1, 1),
                date_added=datetime.date(2010, 1, 1),
                date_completed=None,
            ),
            todo_domain.Yearly(
                todo_id=2,
                user_id=2,
                category=core.TodoCategory.Todo,
                description="Make Bed",
                advance_days=10,
                month=todo_domain.Month(3),
                day=5,
                note="",
                start_date=datetime.date(2009, 1, 1),
                date_added=datetime.date(2009, 1, 2),
                date_completed=datetime.date(2010, 1, 1),
            ),
        ]
    )
    result = asyncio.run(
        update_monthly_todo(
            todo_id=1,
            description="Dust Really Good",
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=1,
        category=core.TodoCategory.Todo,
        description="Dust Really Good",
        frequency="Oct 10",
        next=datetime.date(2010, 10, 10),
        display=True,
        note="",
    )


@freezegun.freeze_time("2010-09-20")
def test_add_one_time_todo_happy_path():
    todo_service = DummyTodoService([])
    result = asyncio.run(
        add_one_time_todo(
            description="Make Bed",
            date=datetime.date(2010, 1, 1),
            note=None,
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=-1,
        category=core.TodoCategory.Todo,
        description="Make Bed",
        frequency="2010-01-01",
        next=datetime.date(2010, 1, 1),
        display=True,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_update_one_time_todo_happy_path():
    todo_service = DummyTodoService(
        [
            todo_domain.Once(
                todo_id=1,
                user_id=1,
                category=core.TodoCategory.Todo,
                description="Dust",
                advance_days=3,
                once_date=datetime.date(2010, 1, 1),
                note="",
                start_date=datetime.date(2010, 1, 1),
                date_added=datetime.date(2010, 1, 1),
                date_completed=None,
            ),
            todo_domain.Once(
                todo_id=2,
                user_id=2,
                category=core.TodoCategory.Todo,
                description="Make Bed",
                advance_days=10,
                once_date=datetime.date(2010, 12, 31),
                note="",
                start_date=datetime.date(2009, 1, 1),
                date_added=datetime.date(2009, 1, 2),
                date_completed=datetime.date(2010, 1, 1),
            ),
        ]
    )
    result = asyncio.run(
        update_one_time_todo(
            todo_id=2,
            description="Make Bed",
            date=datetime.date(2010, 1, 1),
            note=None,
            current_user=auth.User(
                user_id=2,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=2,
        category=core.TodoCategory.Todo,
        description="Make Bed",
        frequency="2010-12-31",
        next=datetime.date(2010, 12, 31),
        display=False,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_add_weekly_todo_happy_path():
    todo_service = DummyTodoService([])
    result = asyncio.run(
        add_weekly_todo(
            description="Make Bed",
            start_date=datetime.date(2010, 1, 1),
            note=None,
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
            week_day=3,
        )
    )
    assert result == api.TodoResponse(
        todo_id=-1,
        category=core.TodoCategory.Todo,
        description="Make Bed",
        frequency="Tue",
        next=datetime.date(2009, 12, 29),
        display=True,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_update_one_time_todo_happy_path():
    todo_service = DummyTodoService(
        [
            todo_domain.Weekly(
                todo_id=1,
                user_id=1,
                category=core.TodoCategory.Todo,
                description="Dust",
                advance_days=3,
                note="",
                start_date=datetime.date(2010, 1, 1),
                date_added=datetime.date(2010, 1, 1),
                date_completed=None,
                week_day=todo_domain.Weekday.Tuesday,
            ),
            todo_domain.Weekly(
                todo_id=2,
                user_id=2,
                category=core.TodoCategory.Todo,
                description="Make Bed",
                advance_days=10,
                note="",
                start_date=datetime.date(2009, 1, 1),
                date_added=datetime.date(2009, 1, 2),
                date_completed=datetime.date(2010, 1, 1),
                week_day=todo_domain.Weekday.Wednesday,
            ),
        ]
    )
    result = asyncio.run(
        update_weekly_todo(
            todo_id=2,
            description="Vaccum",
            current_user=auth.User(
                user_id=2,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=2,
        category=core.TodoCategory.Todo,
        description="Vaccum",
        frequency="Wed",
        next=datetime.date(2010, 1, 6),
        display=False,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_add_xdays_todo_happy_path():
    todo_service = DummyTodoService([])
    result = asyncio.run(
        add_xdays_todo(
            description="Make Bed",
            start_date=datetime.date(2010, 1, 1),
            note=None,
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
            days=3,
        )
    )
    assert result == api.TodoResponse(
        todo_id=-1,
        category=core.TodoCategory.Todo,
        description="Make Bed",
        frequency="Every 3 days",
        next=datetime.date(2010, 1, 4),
        display=False,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_update_xdays_todo_happy_path():
    todo_service = DummyTodoService(
        [
            todo_domain.XDays(
                todo_id=1,
                user_id=1,
                category=core.TodoCategory.Todo,
                description="Dust",
                advance_days=3,
                note="",
                start_date=datetime.date(2010, 1, 1),
                date_added=datetime.date(2010, 1, 1),
                date_completed=None,
                days=3,
            ),
            todo_domain.XDays(
                todo_id=2,
                user_id=2,
                category=core.TodoCategory.Todo,
                description="Make Bed",
                advance_days=10,
                note="",
                start_date=datetime.date(2009, 1, 1),
                date_added=datetime.date(2009, 1, 2),
                date_completed=datetime.date(2010, 1, 1),
                days=4,
            ),
        ]
    )
    result = asyncio.run(
        update_xdays_todo(
            todo_id=2,
            description="Vaccum",
            current_user=auth.User(
                user_id=2,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=2,
        category=core.TodoCategory.Todo,
        description="Vaccum",
        frequency="Every 4 days",
        next=datetime.date(2010, 1, 4),
        display=False,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_add_yearly_todo_happy_path():
    todo_service = DummyTodoService([])
    result = asyncio.run(
        add_yearly_todo(
            description="Make Bed",
            start_date=datetime.date(2010, 1, 1),
            note=None,
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
            month=11,
            day=1,
        )
    )
    assert result == api.TodoResponse(
        todo_id=-1,
        category=core.TodoCategory.Todo,
        description="Make Bed",
        frequency="Nov 1",
        next=datetime.date(2010, 11, 1),
        display=False,
        note="",
    )


@freezegun.freeze_time("2010-01-01")
def test_update_yearly_todo_happy_path():
    todo_service = DummyTodoService(
        [
            todo_domain.Yearly(
                todo_id=1,
                user_id=1,
                category=core.TodoCategory.Todo,
                description="Dust",
                advance_days=3,
                note="",
                start_date=datetime.date(2010, 1, 1),
                date_added=datetime.date(2010, 1, 1),
                date_completed=None,
                month=todo_domain.Month.January,
                day=11,
            ),
            todo_domain.Yearly(
                todo_id=2,
                user_id=2,
                category=core.TodoCategory.Todo,
                description="Make Bed",
                advance_days=10,
                note="",
                start_date=datetime.date(2009, 1, 1),
                date_added=datetime.date(2009, 1, 2),
                date_completed=datetime.date(2010, 1, 1),
                month=todo_domain.Month.October,
                day=1,
            ),
        ]
    )
    result = asyncio.run(
        update_xdays_todo(
            todo_id=2,
            description="Vaccum",
            current_user=auth.User(
                user_id=2,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == api.TodoResponse(
        todo_id=2,
        category=core.TodoCategory.Todo,
        description="Vaccum",
        frequency="Oct 1",
        next=datetime.date(2010, 10, 1),
        display=False,
        note="",
    )


def test_delete_todo():
    todo_service = DummyTodoService(
        [
            todo_domain.Yearly(
                todo_id=1,
                user_id=1,
                category=core.TodoCategory.Todo,
                description="Dust",
                advance_days=3,
                note="",
                start_date=datetime.date(2010, 1, 1),
                date_added=datetime.date(2010, 1, 1),
                date_completed=None,
                month=todo_domain.Month.January,
                day=11,
            ),
            todo_domain.Weekly(
                todo_id=2,
                user_id=2,
                category=core.TodoCategory.Todo,
                description="Make Bed",
                advance_days=10,
                note="",
                start_date=datetime.date(2009, 1, 1),
                date_added=datetime.date(2009, 1, 2),
                date_completed=datetime.date(2010, 1, 1),
                week_day=todo_domain.Weekday.Tuesday,
            ),
        ]
    )
    result = asyncio.run(
        delete_todo(
            todo_id=1,
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result is None


def test_all_todos_happy_path():
    todo_service = DummyTodoService(
        [
            todo_domain.Yearly(
                todo_id=1,
                user_id=1,
                category=core.TodoCategory.Todo,
                description="Dust",
                advance_days=3,
                note="",
                start_date=datetime.date(2010, 1, 1),
                date_added=datetime.date(2010, 1, 1),
                date_completed=None,
                month=todo_domain.Month.January,
                day=11,
            ),
            todo_domain.Weekly(
                todo_id=2,
                user_id=2,
                category=core.TodoCategory.Todo,
                description="Make Bed",
                advance_days=10,
                note="",
                start_date=datetime.date(2009, 1, 1),
                date_added=datetime.date(2009, 1, 2),
                date_completed=datetime.date(2010, 1, 1),
                week_day=todo_domain.Weekday.Tuesday,
            ),
        ]
    )
    result = asyncio.run(
        all_todos(
            current_user=auth.User(
                user_id=1,
                username="test_user",
                email=pydantic.EmailStr("test_user@gmail.com"),
                password_hash="1234" * 15,
            ),
            todo_service=todo_service,
        )
    )
    assert result == [
        api.TodoResponse(
            todo_id=1,
            category=core.TodoCategory.Todo,
            description="Dust",
            frequency="Jan 11",
            next=datetime.date(2021, 1, 11),
            display=True,
            note="",
        ),
        api.TodoResponse(
            todo_id=2,
            category=core.TodoCategory.Todo,
            description="Make Bed",
            frequency="Tue",
            next=datetime.date(2021, 3, 23),
            display=True,
            note="",
        ),
    ]
