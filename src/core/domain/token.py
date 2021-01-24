from __future__ import annotations

import abc
import typing

import pydantic as pydantic

__all__ = ("Token",)


class Token(pydantic.BaseModel, abc.ABC):
    access_token: pydantic.constr(strip_whitespace=True, min_length=1)  # type: ignore
    token_type: typing.Literal["bearer"] = "bearer"
