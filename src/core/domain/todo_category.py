import enum


__all__ = ("TodoCategory",)


class TodoCategory(str, enum.Enum):
    Todo = "todo"
    Reminder = "reminder"

    def __str__(self) -> str:
        return str.__str__(self)
