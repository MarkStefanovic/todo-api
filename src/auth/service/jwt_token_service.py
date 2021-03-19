import datetime
import typing

import jwt
from starlette.datastructures import Secret

from src import core
from src.auth import domain

__all__ = ("JwtTokenService",)


class JwtTokenService(domain.TokenService):
    def __init__(
        self,
        *,
        secret_key: Secret,
        expires_delta: datetime.timedelta,
        algorithm: str,
    ):
        self._secret_key = secret_key
        self._expires_delta = expires_delta
        self._algorithm = algorithm

    def create(self, /, data: typing.Dict[str, typing.Any]) -> domain.Token:
        expire = datetime.datetime.utcnow() + self._expires_delta
        token = jwt.encode(
            payload=data | {"exp": expire},
            key=str(self._secret_key),
            # key=self._secret_key.get_secret_value(),
            algorithm=self._algorithm,
        )
        return domain.Token(
            access_token=token,
            token_type="bearer",
        )

    def username(self, /, token: str) -> str:
        try:
            payload: typing.Dict[str, typing.Any] = jwt.decode(
                jwt=token,
                key=str(self._secret_key),
                # key self._secret_key.get_secret_value(),
                algorithms=[self._algorithm],
            )
        except Exception as e:
            raise core.exception.AuthException(
                f"An error occurred when decoding the jwt token: {e}."
            )

        username: typing.Optional[str] = payload.get("sub")
        if username is None:
            raise core.exception.MalformedTokenException(
                "Token is missing a 'sub' key."
            )
        else:
            return username
