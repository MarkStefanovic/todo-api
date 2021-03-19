import datetime
import typing

from src import core
from src.todo import domain, adapter

__all__ = ("SqlAlchemyTodoService",)


class SqlAlchemyTodoService(domain.TodoService):
    def __init__(self, /, uow: core.SqlAlchemyUnitOfWork):
        self._uow = uow

    def all(self, /, user_id: int) -> typing.List[domain.Todo]:
        with self._uow:
            return self._repo.all(user_id)

    def add_todo(self, *, user_id: int, todo: domain.Todo) -> domain.Todo:
        with self._uow:
            new_todo = self._repo.add(user_id=user_id, item=todo)
            self._uow.commit()
            return new_todo

    def delete_todo(self, *, user_id: int, todo_id: int) -> None:
        with self._uow:
            self._repo.remove(user_id=user_id, item_id=todo_id)
            self._uow.commit()

    def get_by_id(self, *, user_id: int, todo_id: int) -> typing.Optional[domain.Todo]:
        assert todo_id > 0, f"Todo id values should be positive, but got {todo_id!r}."
        with self._uow:
            todo = self._repo.get_by_id(user_id=user_id, todo_id=todo_id)
            if todo and todo.user_id == user_id:
                return todo
            else:
                raise core.exception.AuthException("Todo belongs to another user")

    def get_current_todos(
        self,
        *,
        user_id: int,
        category: str,
        today: datetime.date = datetime.date.today(),
    ) -> typing.List[domain.Todo]:
        return [
            todo
            for todo in self.all(user_id)
            if todo.display(today) and todo.category == category
        ]

    def get_todos_completed_today(
        self, *, user_id: int, today: datetime.date = datetime.date.today()
    ) -> typing.List[domain.Todo]:
        return [todo for todo in self.all(user_id) if todo.date_completed == today]

    def mark_complete(self, *, user_id: int, todo_id: int) -> None:
        with self._uow:
            self._repo.mark_completed(user_id=user_id, item_id=todo_id)
            self._uow.commit()

    def update_todo(self, *, user_id: int, todo: domain.Todo) -> domain.Todo:
        with self._uow:
            updated_todo = self._repo.update(user_id=user_id, item=todo)
            self._uow.commit()
            return updated_todo

    @property
    def _repo(self) -> domain.TodoRepository:
        return adapter.SqlAlchemyTodoRepository(self._uow.session)