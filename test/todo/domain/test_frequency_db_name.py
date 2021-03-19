from src import core

if __name__ == "__main__":
    n = core.FrequencyDbName.DAILY
    assert n == "daily"
    print(n)
    print(repr(n))
    x = core.FrequencyDbName("todo")
