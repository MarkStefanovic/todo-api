from src.todo.domain.weekday import Weekday


def test_weekday() -> None:
    wd = Weekday.Monday
    assert repr(wd) == "<Weekday.Monday: 2>"
    assert str(wd) == "Monday"
    assert wd == 2
