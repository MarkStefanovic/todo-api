import abc
import datetime
import typing

from src.todo.domain import todo as todo_domain

__all__ = ("TodoService",)


class TodoService(abc.ABC):
    @abc.abstractmethod
    def all(self, /, user_id: int) -> typing.List[todo_domain.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_todo(self, *, user_id: int, todo: todo_domain.Todo) -> todo_domain.Todo:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_todo(self, *, user_id: int, todo_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, *, user_id: int, todo_id: int) -> typing.Optional[todo_domain.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_current_todos(
        self,
        *,
        user_id: int,
        category: str,
        today: datetime.date = datetime.date.today(),
    ) -> typing.List[todo_domain.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_todos_completed_today(
        self, *, user_id: int, today: datetime.date = datetime.date.today()
    ) -> typing.List[todo_domain.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_complete(self, *, user_id: int, todo_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update_todo(self, *, user_id: int, todo: todo_domain.Todo) -> todo_domain.Todo:
        raise NotImplementedError
