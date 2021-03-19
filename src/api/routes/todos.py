import datetime
import typing

import fastapi
import pydantic
from starlette.status import HTTP_400_BAD_REQUEST

from src import auth, todo, core, service_locator
from src.api import response
from src.api.routes import get_current_active_user

__all__ = ("router",)

router = fastapi.APIRouter()


def update_todo(
    *,
    user_id: int,
    todo_id: int,
    todo_service: todo.TodoService,
    updates: typing.Dict[str, typing.Any],
) -> response.TodoResponse:
    original_todo = todo_service.get_by_id(user_id=user_id, todo_id=todo_id)
    if original_todo:
        data = original_todo.dict()
        data.update(updates)
        _, _, errors = pydantic.validate_model(todo.Todo, data)
        if errors:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail=errors.json(),
            )

        updated_todo = original_todo.copy(update=updates)
        updated_todo_from_db = todo_service.update_todo(user_id=user_id, todo=updated_todo)
        return response.TodoResponse.from_domain(updated_todo_from_db)
    else:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Todo does not exist.")


@router.post("/daily", response_model=response.TodoResponse, status_code=201)
async def add_daily_todo(
    description: str,
    note: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    if start_date is None:
        start_date = datetime.date.today()
    if note is None:
        note = ""
    daily_todo = todo.Daily(
        advance_days=0,
        category=core.TodoCategory.Todo,
        date_added=datetime.date.today(),
        date_completed=None,
        description=description,
        note=note,
        start_date=start_date,
        todo_id=-1,
        user_id=current_user.user_id,
    )
    new_todo = todo_service.add_todo(user_id=current_user.user_id, todo=daily_todo)
    return response.TodoResponse.from_domain(new_todo)


@router.post("/daily/{todo_id}", response_model=response.TodoResponse)
async def update_daily_todo(
    todo_id: int,
    description: typing.Optional[str] = None,
    note: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    updates: typing.Dict[str, typing.Any] = {}
    if start_date is None:
        updates["start_date"] = start_date
    if description is not None:
        updates["description"] = description
    if note is not None:
        updates["note"] = note

    return update_todo(
        user_id=current_user.user_id,
        todo_id=todo_id,
        todo_service=todo_service,
        updates=updates,
    )


@router.post("/irregular", response_model=response.TodoResponse, status_code=201)
async def add_irregular_todo(
    description: str,
    advance_days: int,
    month: int,
    week_day: int,
    week: int,
    note: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    validation_errors: typing.List[str] = []
    if month not in range(1, 12):
        validation_errors.append("month must be between 1 and 12")
    if week_day not in range(1, 7):
        validation_errors.append("week_day must be between 1 and 7")
    if week not in range(1, 5):
        validation_errors.append("week must be between 1 and 5")
    if validation_errors:
        errors_str = "; ".join(validation_errors)
        msg = f"Validation errors: {errors_str}"
        raise fastapi.HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=msg)
    if start_date is None:
        start_date = datetime.date.today()
    if note is None:
        note = ""
    irregular_todo = todo.Irregular(
        advance_days=advance_days,
        category=core.TodoCategory.Todo,
        date_added=datetime.date.today(),
        date_completed=None,
        description=description,
        note=note,
        start_date=start_date,
        todo_id=-1,
        user_id=current_user.user_id,
        month=todo.Month(month),
        week_day=todo.Weekday(week_day),
        week_number=week,
    )
    new_todo = todo_service.add_todo(user_id=current_user.user_id, todo=irregular_todo)
    return response.TodoResponse.from_domain(new_todo)


@router.post("/irregular/{todo_id}", response_model=response.TodoResponse)
async def update_irregular_todo(
    todo_id: int,
    description: typing.Optional[str] = None,
    advance_days: typing.Optional[int] = None,
    month: typing.Optional[int] = None,
    week_day: typing.Optional[int] = None,
    week: typing.Optional[int] = None,
    note: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    updates: typing.Dict[str, typing.Any] = {}
    if description is not None:
        updates["description"] = description
    if advance_days is not None:
        updates["advance_days"] = advance_days
    if month is not None:
        updates["month"] = month
    if week_day is not None:
        updates["week_day"] = week_day
    if week is not None:
        updates["week"] = week
    if note is not None:
        updates["note"] = note
    if start_date is not None:
        updates["start_date"] = start_date

    return update_todo(
        user_id=current_user.user_id,
        todo_id=todo_id,
        todo_service=todo_service,
        updates=updates,
    )


@router.post("/monthly", response_model=response.TodoResponse, status_code=201)
async def add_monthly_todo(
    description: str,
    advance_days: int,
    month_day: int,
    note: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    if month_day not in range(1, 28):
        raise fastapi.HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="month_day must be between 1 and 28",
        )

    if start_date is None:
        start_date = datetime.date.today()
    if note is None:
        note = ""
    monthly_todo = todo.Monthly(
        advance_days=advance_days,
        category=core.TodoCategory.Todo,
        date_added=datetime.date.today(),
        date_completed=None,
        description=description,
        note=note,
        start_date=start_date,
        todo_id=-1,
        user_id=current_user.user_id,
        month_day=month_day,
    )
    new_todo = todo_service.add_todo(user_id=current_user.user_id, todo=monthly_todo)
    return response.TodoResponse.from_domain(new_todo)


@router.post("/monthly/{todo_id}", response_model=response.TodoResponse)
async def update_monthly_todo(
    todo_id: int,
    description: typing.Optional[str] = None,
    advance_days: typing.Optional[int] = None,
    month_day: typing.Optional[int] = None,
    note: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    if month_day and month_day not in range(1, 28):
        raise fastapi.HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="month_day must be between 1 and 28",
        )

    updates: typing.Dict[str, typing.Any] = {}
    if description is not None:
        updates["description"] = description
    if advance_days is not None:
        updates["advance_days"] = advance_days
    if month_day is not None:
        updates["month_day"] = month_day
    if note is not None:
        updates["note"] = note
    if start_date is not None:
        updates["start_date"] = start_date

    return update_todo(
        user_id=current_user.user_id,
        todo_id=todo_id,
        todo_service=todo_service,
        updates=updates,
    )


@router.post("/once", response_model=response.TodoResponse, status_code=201)
async def add_one_time_todo(
    description: str,
    date: datetime.date,
    note: typing.Optional[str] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    if note is None:
        note = ""
    once_todo = todo.Once(
        advance_days=0,
        category=core.TodoCategory.Todo,
        date_added=datetime.date.today(),
        date_completed=None,
        description=description,
        note=note,
        start_date=date,
        once_date=date,
        todo_id=-1,
        user_id=current_user.user_id,
    )
    new_todo = todo_service.add_todo(user_id=current_user.user_id, todo=once_todo)
    return response.TodoResponse.from_domain(new_todo)


@router.post("/once", response_model=response.TodoResponse)
async def update_one_time_todo(
    todo_id: int,
    description: typing.Optional[str] = None,
    date: typing.Optional[datetime.date] = None,
    note: typing.Optional[str] = None,
    advance_days: typing.Optional[int] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    updates: typing.Dict[str, typing.Any] = {}
    if description is not None:
        updates["description"] = description
    if advance_days is not None:
        updates["advance_days"] = advance_days
    if note is not None:
        updates["note"] = note
    if date is not None:
        updates["date"] = date

    return update_todo(
        user_id=current_user.user_id,
        todo_id=todo_id,
        todo_service=todo_service,
        updates=updates,
    )


@router.post("/weekly", response_model=response.TodoResponse, status_code=201)
async def add_weekly_todo(
    description: str,
    start_date: datetime.date,
    week_day: int,
    note: typing.Optional[str] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    if note is None:
        note = ""
    weekly_todo = todo.Weekly(
        advance_days=0,
        category=core.TodoCategory.Todo,
        date_added=datetime.date.today(),
        date_completed=None,
        description=description,
        note=note,
        start_date=start_date,
        todo_id=-1,
        user_id=current_user.user_id,
        week_day=todo.Weekday(week_day),
    )
    new_todo = todo_service.add_todo(user_id=current_user.user_id, todo=weekly_todo)
    return response.TodoResponse.from_domain(new_todo)


@router.post("/weekly/{todo_id}", response_model=response.TodoResponse)
async def update_weekly_todo(
    todo_id: int,
    description: typing.Optional[str] = None,
    date: typing.Optional[datetime.date] = None,
    week_day: typing.Optional[int] = None,
    note: typing.Optional[str] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    updates: typing.Dict[str, typing.Any] = {}
    if description is not None:
        updates["description"] = description
    if week_day is not None:
        updates["week_day"] = week_day
    if note is not None:
        updates["note"] = note
    if date is not None:
        updates["date"] = date

    return update_todo(
        user_id=current_user.user_id,
        todo_id=todo_id,
        todo_service=todo_service,
        updates=updates,
    )


@router.post("/xdays", response_model=response.TodoResponse, status_code=201)
async def add_xdays_todo(
    description: str,
    start_date: datetime.date,
    days: int,
    note: typing.Optional[str] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    if note is None:
        note = ""
    xdays_todo = todo.XDays(
        advance_days=0,
        category=core.TodoCategory.Todo,
        date_added=datetime.date.today(),
        date_completed=None,
        description=description,
        note=note,
        start_date=start_date,
        todo_id=-1,
        user_id=current_user.user_id,
        days=days,
    )
    new_todo = todo_service.add_todo(user_id=current_user.user_id, todo=xdays_todo)
    return response.TodoResponse.from_domain(new_todo)


@router.post("/xdays/{todo_id}", response_model=response.TodoResponse)
async def update_xdays_todo(
    todo_id: int,
    description: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    days: typing.Optional[int] = None,
    note: typing.Optional[str] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    updates: typing.Dict[str, typing.Any] = {}
    if description is not None:
        updates["description"] = description
    if days is not None:
        updates["days"] = days
    if note is not None:
        updates["note"] = note
    if start_date is not None:
        updates["date"] = start_date

    return update_todo(
        user_id=current_user.user_id,
        todo_id=todo_id,
        todo_service=todo_service,
        updates=updates,
    )


@router.post("/yearly", response_model=response.TodoResponse, status_code=201)
async def add_yearly_todo(
    description: str,
    start_date: datetime.date,
    month: int,
    day: int,
    note: typing.Optional[str] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    validation_errors: typing.List[str] = []
    if month not in range(1, 12):
        validation_errors.append("month must be between 1 and 12")
    if day not in range(1, 31):
        validation_errors.append("day must be between 1 and 31")
    if validation_errors:
        errors_str = "; ".join(validation_errors)
        msg = f"Validation errors: {errors_str}"
        raise fastapi.HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=msg)
    if note is None:
        note = ""
    yearly_todo = todo.Yearly(
        advance_days=0,
        category=core.TodoCategory.Todo,
        date_added=datetime.date.today(),
        date_completed=None,
        description=description,
        note=note,
        start_date=start_date,
        todo_id=-1,
        user_id=current_user.user_id,
        day=day,
        month=todo.Month(month),
    )
    new_todo = todo_service.add_todo(user_id=current_user.user_id, todo=yearly_todo)
    return response.TodoResponse.from_domain(new_todo)


@router.post("/yearly/{todo_id}", response_model=response.TodoResponse)
async def update_yearly_todo(
    todo_id: int,
    description: typing.Optional[str] = None,
    start_date: typing.Optional[datetime.date] = None,
    month: typing.Optional[int] = None,
    day: typing.Optional[int] = None,
    note: typing.Optional[str] = None,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> response.TodoResponse:
    updates: typing.Dict[str, typing.Any] = {}
    if description is not None:
        updates["description"] = description
    if month is not None:
        updates["month"] = month
    if day is not None:
        updates["day"] = month
    if note is not None:
        updates["note"] = note
    if start_date is not None:
        updates["date"] = start_date

    return update_todo(
        user_id=current_user.user_id,
        todo_id=todo_id,
        todo_service=todo_service,
        updates=updates,
    )


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> None:
    todo_service.delete_todo(user_id=current_user.user_id, todo_id=todo_id)


@router.get("")
async def all_todos(
    current_user: auth.User = fastapi.Depends(get_current_active_user),
    todo_service: todo.TodoService = fastapi.Depends(
        service_locator.default().todo_service
    ),
) -> typing.List[response.TodoResponse]:
    todos = todo_service.all(current_user.user_id)
    return [response.TodoResponse.from_domain(t) for t in todos]
