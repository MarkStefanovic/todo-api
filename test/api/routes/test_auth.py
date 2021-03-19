import asyncio
import dataclasses
import typing

import pydantic

from src import auth, api
from src.api.routes import get_current_active_user
from src.api.routes.auth import login, get_user, register
from src.auth import domain


def dummy_hasher(plain_password: pydantic.SecretStr) -> str:
    return plain_password.get_secret_value() * 15


PASSWORD = pydantic.SecretStr("1234")
PASSWORD_HASH = dummy_hasher(PASSWORD)
ACCESS_TOKEN = "test_user." + PASSWORD_HASH


class DummyPasswordHasher(auth.PasswordHashService):
    def create(self, /, plain_password: pydantic.SecretStr) -> str:
        return dummy_hasher(plain_password)

    def verify(
        self, *, hashed_password: str, plain_password: pydantic.SecretStr
    ) -> bool:
        return dummy_hasher(plain_password) == hashed_password


class DummyTokenService(auth.TokenService):
    def create(self, /, data: typing.Dict[str, typing.Any]) -> domain.Token:
        return domain.Token(access_token=ACCESS_TOKEN, token_type="bearer")

    def username(self, /, token: str) -> str:
        assert isinstance(token, str)
        return token.split(".")[0]


class DummyUserService(auth.UserService):
    def create_user(
        self, *, username: str, email: pydantic.EmailStr, password_hash: str
    ) -> domain.User:
        return domain.User(
            user_id=1,
            username=username,
            email=email,
            password_hash=password_hash,
        )

    def get_user(self, /, username: str) -> domain.User:
        return domain.User(
            user_id=1,
            username="test_user",
            email=pydantic.EmailStr("test_user@gmail.com"),
            password_hash=PASSWORD_HASH,
        )

    def remove_user(self, username: str) -> None:
        pass


@dataclasses.dataclass
class MockOAuth2PasswordRequestForm:
    username: str
    password: str


def test_get_current_active_user_happy_path() -> None:
    token_service = DummyTokenService()
    user_service = DummyUserService()

    user = get_current_active_user(
        token=ACCESS_TOKEN, token_service=token_service, user_service=user_service
    )
    assert user == auth.User(
        user_id=1,
        username="test_user",
        email=pydantic.EmailStr("test_user@gmail.com"),
        password_hash=PASSWORD_HASH,
    )


def test_login_happy_path():
    form_data = MockOAuth2PasswordRequestForm(
        username="test_user", password=PASSWORD.get_secret_value()
    )
    user_service = DummyUserService()
    password_hasher = DummyPasswordHasher()
    token_service = DummyTokenService()
    result = asyncio.run(
        login(
            form_data=form_data,
            user_service=user_service,
            password_hasher=password_hasher,
            token_service=token_service,
        )
    )
    assert result == auth.Token(
        access_token=ACCESS_TOKEN,
        token_type="bearer",
    )


def test_get_user_happy_path():
    current_user = auth.User(
        user_id=1,
        username="test_user",
        email=pydantic.EmailStr("test_user@gmail.com"),
        password_hash=PASSWORD_HASH,
    )
    result = asyncio.run(get_user(current_user))
    assert result == api.UserResponse(
        username="test_user",
        email="test_user@gmail.com",
    )


def test_register_happy_path():
    username = "test_user"
    email = pydantic.EmailStr("test_user@gmail.com")
    password = "1234"
    user_service = DummyUserService()
    password_hasher = DummyPasswordHasher()

    result = asyncio.run(
        register(
            username=username,
            email=email,
            password=password,
            user_service=user_service,
            password_hasher=password_hasher,
        )
    )
    assert result == api.UserResponse(username=username, email=email)
