import enum

__all__ = ("FrequencyDbName",)


class FrequencyDbName(str, enum.Enum):
    DAILY = "daily"
    EASTER = "easter"
    IRREGULAR = "irregular"
    MONTHLY = "monthly"
    ONCE = "once"
    WEEKLY = "weekly"
    XDAYS = "xdays"
    YEARLY = "yearly"

    def __str__(self) -> str:
        return str.__str__(self)
