import pydantic
import pytest
import sqlalchemy as sa
from sqlalchemy import orm

from src.core import adapter, domain

USERS = [
    adapter.UserDTO(
        id=1,
        username="marks",
        email="marks@test.com",
        active=True,
        password_hash="a" * 60,
    ),
    adapter.UserDTO(
        id=2,
        username="lillie.block",
        email="mary.marks@gmail.com",
        active=True,
        password_hash="b" * 60,
    ),
    adapter.UserDTO(
        id=3,
        username="winford.oconnell",
        email="berenice.toy@gmail.com",
        active=True,
        password_hash="c" * 60,
    ),
]


@pytest.fixture(scope="function")
def session() -> orm.Session:
    engine = sa.create_engine("sqlite://")
    adapter.db_schema.Base.metadata.create_all(engine)
    session_factory = orm.sessionmaker(bind=engine)
    session: orm.Session = session_factory()
    session.add_all(USERS)
    session.commit()
    return session_factory()


def test_add_user(session: orm.Session) -> None:
    row_ct = session.execute("SELECT COUNT(*) FROM user").scalar()
    assert row_ct == len(USERS)

    user_repo = adapter.SqlalchemyUserRepo(session)
    user_repo.add_user(
        username="stevesmith",
        email=pydantic.EmailStr("stevesmith@testemail.com"),
        password_hash="d" * 60,
    )
    session.commit()

    row_ct = session.execute("SELECT COUNT(*) FROM user").scalar()
    assert row_ct == len(USERS) + 1

    user = session.query(adapter.UserDTO).filter_by(username="stevesmith").first()
    assert user.email == "stevesmith@testemail.com"
    assert user.password_hash == "d" * 60


def test_get_user(session: orm.Session) -> None:
    user_repo = adapter.SqlalchemyUserRepo(session)
    actual_user = user_repo.get_user("marks")
    assert actual_user.email == "marks@test.com"


def test_retire_user(session: orm.Session) -> None:
    user_dto = session.query(adapter.UserDTO).filter_by(username="marks").first()
    assert user_dto.active is True
    user_repo = adapter.SqlalchemyUserRepo(session)
    user_repo.retire_user("marks")
    user_dto = session.query(adapter.UserDTO).filter_by(username="marks").first()
    assert user_dto.active is False
