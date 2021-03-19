from __future__ import annotations

import pydantic

__all__ = ("User",)


class User(pydantic.BaseModel):
    user_id: int
    username: str
    email: pydantic.EmailStr
    password_hash: pydantic.constr(strip_whitespace=True, min_length=60, max_length=60)  # type: ignore
