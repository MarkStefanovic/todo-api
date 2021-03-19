import typing

import pydantic
import pytest
from sqlalchemy import orm

from src import core, auth


@pytest.fixture(scope="function")
def default_users() -> typing.List[core.UserDTO]:
    return [
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
        core.UserDTO(
            user_id=3,
            username="winford.oconnell",
            email="berenice.toy@gmail.com",
            password_hash="c" * 60,
        ),
    ]


def test_add_user(session: orm.Session, default_users: typing.List[core.UserDTO]) -> None:
    session.add_all(default_users)
    session.commit()

    row_ct = session.execute("SELECT COUNT(*) FROM auth.user").scalar()
    assert row_ct == len(default_users)

    user_repo = auth.SqlalchemyUserRepository(session)
    user_repo.add_user(
        username="stevesmith",
        email=pydantic.EmailStr("stevesmith@testemail.com"),
        password_hash="d" * 60,
    )
    session.commit()

    row_ct = session.execute("SELECT COUNT(*) FROM auth.user").scalar()
    assert row_ct == len(default_users) + 1

    user = session.query(core.UserDTO).filter_by(username="stevesmith").first()
    assert user is not None
    assert user.email == "stevesmith@testemail.com"
    assert user.password_hash == "d" * 60


def test_get_user(session: orm.Session, default_users: typing.List[core.UserDTO]) -> None:
    session.add_all(default_users)
    session.commit()

    user_repo = auth.SqlalchemyUserRepository(session)
    actual_user = user_repo.get_user("marks")
    assert actual_user is not None
    assert actual_user.email == "marks@test.com"


def test_remove_user(session: orm.Session, default_users: typing.List[core.UserDTO]) -> None:
    session.add_all(default_users)
    session.commit()

    user_dto = session.query(core.UserDTO).filter_by(username="marks").first()
    assert user_dto is not None
    user_repo = auth.SqlalchemyUserRepository(session)
    user_repo.remove_user("marks")
    user_dto = session.query(core.UserDTO).filter_by(username="marks").first()
    assert user_dto is None
