import datetime

import pytest
import sqlalchemy as sa
from sqlalchemy import orm

import src.todo.adapter.sqlalchemy_todo_repository
from src import core, todo

from test.test_utils.sa_test_utils import *


# from src import core, auth, todo
#
USERS = [
    core.UserDTO(
        user_id=1,
        username="marks",
        email="marks@test.com",
        password_hash="a" * 60,
    ),
    core.UserDTO(
        user_id=2,
        username="lillie.block",
        email="mary.marks@gmail.com",
        password_hash="b" * 60,
    ),
]


def test_sqlalchemy_todo_repository_add(session: orm.Session) -> None:
    initial_ct = session.query(core.TodoDTO).count()
    assert initial_ct == 0

    repo = todo.SqlAlchemyTodoRepository(session)
    new_todo = todo.Weekly(
        advance_days=10,
        category=core.TodoCategory.Todo,
        date_added=datetime.date(2010, 1, 2),
        date_completed=None,
        description="Vacuum",
        note="",
        start_date=None,
        todo_id=1,
        user_id=1,
        week_day=todo.Weekday.Sunday,
    )
    result = repo.add(user_id=1, item=new_todo)

    after_insert_ct = session.query(core.TodoDTO).count()
    assert after_insert_ct == 1

    actual_dto = session.query(core.TodoDTO).first()
    assert actual_dto is not None
    expected_dto: core.TodoDTO = src.todo.adapter.sqlalchemy_todo_repository.from_domain(result)
    assert dto_to_dict(actual_dto) == dto_to_dict(expected_dto)


def test_sqlalchemy_todo_repository_all(session: orm.Session) -> None:
    initial_ct = session.query(core.TodoDTO).count()
    assert initial_ct == 0

    todo_dtos = [
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=1,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Grocery Shopping",
                note="",
                start_date=None,
                todo_id=1,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Brush Teeth",
                note="",
                start_date=None,
                todo_id=2,
                user_id=2,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=2,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Vacuum",
                note="",
                start_date=None,
                todo_id=3,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
    ]
    session.add_all(todo_dtos)
    session.commit()

    repo = todo.SqlAlchemyTodoRepository(session)
    actual = repo.all(user_id=1)
    assert len(actual) == 2
    actual_descriptions = sorted(dto.description for dto in actual)
    assert actual_descriptions == ["Grocery Shopping", "Vacuum"]


def test_sqlalchemy_todo_repository_get_by_id(session: orm.Session) -> None:
    initial_ct = session.query(core.TodoDTO).count()
    assert initial_ct == 0

    todo_dtos = [
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=1,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Grocery Shopping",
                note="",
                start_date=None,
                todo_id=1,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Brush Teeth",
                note="",
                start_date=None,
                todo_id=2,
                user_id=2,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=2,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Vacuum",
                note="",
                start_date=None,
                todo_id=3,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
    ]
    session.add_all(todo_dtos)
    session.commit()

    repo = todo.SqlAlchemyTodoRepository(session)
    actual = repo.get_by_id(user_id=2, todo_id=2)
    assert actual is not None
    assert actual.description == "Brush Teeth"


def test_sqlalchemy_todo_repository_mark_completed(session: orm.Session) -> None:
    initial_ct = session.query(core.TodoDTO).count()
    assert initial_ct == 0

    todo_dtos = [
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=1,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Grocery Shopping",
                note="",
                start_date=None,
                todo_id=1,
                user_id=1,
                week_day=todo.Weekday.Sunday
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Brush Teeth",
                note="",
                start_date=None,
                todo_id=2,
                user_id=2,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=2,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Vacuum",
                note="",
                start_date=None,
                todo_id=3,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
    ]
    session.add_all(todo_dtos)
    session.commit()

    repo = todo.SqlAlchemyTodoRepository(session)
    repo.mark_completed(user_id=2, item_id=2, today=datetime.date(2020, 12, 31))
    session.commit()

    actual = session.query(core.TodoDTO).filter_by(todo_id=2).first()
    assert actual is not None
    assert actual.date_completed == datetime.date(2020, 12, 31)


def test_sqlalchemy_todo_repository_remove(session: orm.Session) -> None:
    initial_ct = session.query(core.TodoDTO).count()
    assert initial_ct == 0

    todo_dtos = [
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=1,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Grocery Shopping",
                note="",
                start_date=None,
                todo_id=1,
                user_id=1,
                week_day=todo.Weekday.Sunday
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Brush Teeth",
                note="",
                start_date=None,
                todo_id=2,
                user_id=2,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=2,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Vacuum",
                note="",
                start_date=None,
                todo_id=3,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
    ]
    session.add_all(todo_dtos)
    session.commit()

    repo = todo.SqlAlchemyTodoRepository(session)
    repo.remove(user_id=2, item_id=2)
    session.commit()

    actual_ct = session.query(core.TodoDTO).filter_by(todo_id=2).count()
    assert actual_ct == 0


def test_sqlalchemy_todo_repository_update(session: orm.Session) -> None:
    initial_ct = session.query(core.TodoDTO).count()
    assert initial_ct == 0

    todo_dtos = [
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=1,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Grocery Shopping",
                note="",
                start_date=None,
                todo_id=1,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=0,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Brush Teeth",
                note="",
                start_date=None,
                todo_id=2,
                user_id=2,
                week_day=todo.Weekday.Sunday,
            )
        ),
        src.todo.adapter.sqlalchemy_todo_repository.from_domain(
            todo.Weekly(
                advance_days=2,
                category=core.TodoCategory.Todo,
                date_added=datetime.date(2010, 1, 2),
                date_completed=None,
                description="Vacuum",
                note="",
                start_date=None,
                todo_id=3,
                user_id=1,
                week_day=todo.Weekday.Sunday,
            )
        ),
    ]
    session.add_all(todo_dtos)
    session.commit()

    updated_todo = todo.Weekly(
        advance_days=0,
        category=core.TodoCategory.Todo,
        date_added=datetime.date(2010, 1, 2),
        date_completed=None,
        description="Fly a Kite",
        note="",
        start_date=None,
        todo_id=2,
        user_id=2,
        week_day=todo.Weekday.Sunday,
    )

    repo = todo.SqlAlchemyTodoRepository(session)
    repo.update(user_id=2, item=updated_todo)
    session.commit()

    actual = session.query(core.TodoDTO).filter_by(todo_id=2).first()
    assert actual is not None
    assert actual.description == "Fly a Kite"
