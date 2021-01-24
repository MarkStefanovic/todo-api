import pydantic

__all__ = ("User",)


class User(pydantic.BaseModel):
    id: int
    username: str
    email: pydantic.EmailStr
    active: bool
    password_hash: pydantic.constr(strip_whitespace=True, min_length=60, max_length=60)  # type: ignore
