import logging

import pytest
import sqlalchemy as sa
from sqlalchemy import orm
from starlette.config import environ

from src import core

logger = logging.getLogger("test")

environ["DB_URL"] = "sqlite://"
environ["SECRET_KEY"] = "1234567890"
environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"


@pytest.fixture(scope="function")
def session() -> orm.Session:
    engine = sa.create_engine("sqlite://", echo=True)
    engine.execute("ATTACH DATABASE ':memory:' AS auth")
    engine.execute("ATTACH DATABASE ':memory:' AS todo")
    core.Base.metadata.create_all(engine)
    session_factory = orm.sessionmaker(bind=engine)
    session: orm.Session = session_factory()
    return session
