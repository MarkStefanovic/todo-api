import pydantic

from src import core
from src.auth import domain, adapter

__all__ = ("SqlalchemyUserService",)


class SqlalchemyUserService(domain.UserService):
    def __init__(self, /, uow: core.SqlAlchemyUnitOfWork):
        self._uow = uow

    def create_user(
        self,
        *,
        username: str,
        email: pydantic.EmailStr,
        password_hash: str,
    ) -> domain.User:
        with self._uow:
            if self._repo.get_user(username):
                raise core.exception.UserAlreadyExists(
                    f"The username {username!r} is already in use."
                )

            self._repo.add_user(
                username=username, email=email, password_hash=password_hash
            )
            self._uow.commit()
            return self.get_user(username)

    def get_user(self, /, username: str) -> domain.User:
        with self._uow:
            maybe_user = self._repo.get_user(username)
            if maybe_user is None:
                raise core.exception.CredentialsException("User not found")
            else:
                return maybe_user

    def remove_user(self, /, username: str) -> None:
        with self._uow:
            return self._repo.remove_user(username)

    @property
    def _repo(self) -> adapter.SqlalchemyUserRepository:
        return adapter.SqlalchemyUserRepository(self._uow.session)
