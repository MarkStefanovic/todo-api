import datetime
import typing

from sqlalchemy import orm

from src import core
from src.todo import domain

__all__ = ("SqlAlchemyTodoRepository",)


class SqlAlchemyTodoRepository(domain.TodoRepository):
    def __init__(self, /, session: orm.Session):
        self._session = session

    def add(self, *, user_id: int, item: domain.Todo) -> domain.Todo:
        dto = from_domain(item)
        dto.user_id = user_id
        self._session.add(dto)
        self._session.flush()
        return to_domain(dto)

    def all(self, /, user_id: int) -> typing.List[domain.Todo]:
        return [
            to_domain(dto)
            for dto in self._session.query(core.TodoDTO).filter_by(user_id=user_id)
        ]

    def get_by_id(self, *, user_id: int, todo_id: int) -> typing.Optional[domain.Todo]:
        dto = self._session.query(core.TodoDTO).filter_by(user_id=user_id, todo_id=todo_id).first()
        if dto:
            return to_domain(dto)
        else:
            return None

    def mark_completed(
        self, *, user_id: int, item_id: int, today: datetime.date = datetime.date.today()
    ) -> None:
        self._session.query(core.TodoDTO).filter_by(user_id=user_id, todo_id=item_id).update(
            {core.TodoDTO.date_completed: today}
        )

    def remove(self, *, user_id: int, item_id: int) -> None:
        self._session.query(core.TodoDTO).filter_by(user_id=user_id, todo_id=item_id).delete()

    def update(self, *, user_id: int, item: domain.Todo) -> domain.Todo:
        dto = from_domain(item)
        self._session.query(core.TodoDTO).filter_by(user_id=user_id, todo_id=item.todo_id).update(
            {
                core.TodoDTO.advance_days: dto.advance_days,
                core.TodoDTO.date_completed: dto.date_completed,
                core.TodoDTO.days: dto.days,
                core.TodoDTO.description: dto.description,
                core.TodoDTO.month: dto.month,
                core.TodoDTO.month_day: dto.month_day,
                core.TodoDTO.note: dto.note,
                core.TodoDTO.start_date: dto.start_date,
                core.TodoDTO.category: dto.category,
                core.TodoDTO.week_day: dto.week_day,
                core.TodoDTO.week_number: dto.week_number,
                core.TodoDTO.year: dto.year,
                core.TodoDTO.frequency: dto.frequency,
            }
        )
        self._session.flush()
        return to_domain(dto)


def from_domain(todo: domain.Todo) -> core.TodoDTO:
    month: typing.Optional[int] = None
    month_day: typing.Optional[int] = None
    week_day: typing.Optional[int] = None
    week_number: typing.Optional[int] = None
    year: typing.Optional[int] = None
    days: typing.Optional[int] = None

    if isinstance(todo, domain.Daily):
        frequency = "daily"
    elif isinstance(todo, domain.Easter):
        frequency = "easter"
    elif isinstance(todo, domain.Irregular):
        month = todo.month
        week_day = todo.week_day.value
        week_number = todo.week_number
        frequency = "irregular"
    elif isinstance(todo, domain.Monthly):
        month_day = todo.month_day
        frequency = "monthly"
    elif isinstance(todo, domain.Once):
        frequency = "once"
    elif isinstance(todo, domain.Weekly):
        week_day = todo.week_day
        frequency = "weekly"
    elif isinstance(todo, domain.XDays):
        days = todo.days
        frequency = "xdays"
    elif isinstance(todo, domain.Yearly):
        month = todo.month
        month_day = todo.day
        frequency = "yearly"
    else:
        raise ValueError(f"Unrecognized frequency: {todo!r}.")

    if todo.todo_id == -1:
        return core.TodoDTO(
            user_id=todo.user_id,
            description=todo.description,
            frequency=frequency,
            year=year,
            month=month,
            month_day=month_day,
            week_day=week_day,
            week_number=week_number,
            date_added=todo.date_added,
            date_completed=todo.date_completed,
            advance_days=todo.advance_days,
            start_date=todo.start_date,
            days=days,
            note=todo.note,
            category=todo.category.value,
        )
    else:
        return core.TodoDTO(
            todo_id=todo.todo_id,
            user_id=todo.user_id,
            description=todo.description,
            frequency=frequency,
            year=year,
            month=month,
            month_day=month_day,
            week_day=week_day,
            week_number=week_number,
            date_added=todo.date_added,
            date_completed=todo.date_completed,
            advance_days=todo.advance_days,
            start_date=todo.start_date,
            days=days,
            note=todo.note,
            category=todo.category.value,
        )


def to_domain(dto: core.TodoDTO) -> domain.Todo:
    if dto.frequency == core.FrequencyDbName.DAILY:
        return domain.Daily(
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
        )
    elif dto.frequency == core.FrequencyDbName.EASTER:
        return domain.Easter(
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
        )
    elif dto.frequency == core.FrequencyDbName.IRREGULAR:
        assert dto.month is not None
        assert dto.week_number is not None
        assert dto.week_day is not None
        return domain.Irregular(
            month=domain.Month(dto.month),
            week_number=dto.week_number,
            week_day=domain.Weekday(dto.week_day),
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
        )
    elif dto.frequency == core.FrequencyDbName.MONTHLY:
        assert dto.month_day is not None
        return domain.Monthly(
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
            month_day=dto.month_day,
        )
    elif dto.frequency == core.FrequencyDbName.ONCE:
        assert dto.start_date is not None
        return domain.Once(
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
            once_date=dto.start_date,
        )
    elif dto.frequency == core.FrequencyDbName.WEEKLY:
        assert dto.week_day is not None
        return domain.Weekly(
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
            week_day=domain.Weekday(dto.week_day),
        )
    elif dto.frequency == core.FrequencyDbName.XDAYS:
        assert dto.days is not None
        assert dto.start_date is not None
        return domain.XDays(
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
            days=dto.days,
        )
    elif dto.frequency == core.FrequencyDbName.YEARLY:
        assert dto.month_day is not None
        assert dto.month is not None
        return domain.Yearly(
            advance_days=dto.advance_days,
            category=dto.category,
            date_added=dto.date_added,
            date_completed=dto.date_completed,
            description=dto.description,
            note=dto.note,
            start_date=dto.start_date,
            todo_id=dto.todo_id,
            user_id=dto.user_id,
            day=dto.month_day,
            month=domain.Month(dto.month),
        )
    else:
        raise ValueError(f"Unrecognized frequency: {dto.frequency!r}.")