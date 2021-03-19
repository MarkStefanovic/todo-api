import abc
import datetime
import typing

from src.todo.domain import todo


__all__ = ("TodoRepository",)


class TodoRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, *, user_id: int, item: todo.Todo) -> todo.Todo:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self, /, user_id: int) -> typing.List[todo.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, *, user_id: int, todo_id: int) -> typing.Optional[todo.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_completed(
        self, *, user_id: int, item_id: int, today: datetime.date = datetime.date.today()
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, *, user_id: int, item_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, user_id: int, item: todo.Todo) -> todo.Todo:
        raise NotImplementedError
