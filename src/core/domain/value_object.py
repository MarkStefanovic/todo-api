# from __future__ import annotations
#
# import typing
#
#
# __all__ = (
#     "DatabaseName",
#     "DatabasePort",
#     "DatabaseServer",
#     "DatabaseUsername",
#     "DbUrl",
#     "NonEmptyStr",
#     "OpaqueNonEmptyStr",
#     "OpaqueValueObject",
#     "Password",
#     "PasswordHash",
#     "PositiveInt",
#     "PostgresDbUrl",
#     "ValueObject",
# )
#
#
# T = typing.TypeVar("T")
#
#
# class ValueObject(typing.Generic[T]):
#     __slots__ = ("_value",)
#
#     def __init__(self, /, value: T):
#         self._value = value
#
#     @property
#     def value(self) -> T:
#         return self._value
#
#     def __eq__(self, other: ValueObject[T]):
#         if other.__class__ is self.__class__:
#             return self._value == typing.cast(ValueObject, other).value
#         else:
#             return NotImplemented
#
#     def __ne__(self, other: ValueObject[T]) -> bool:
#         result = self.__eq__(other)
#         if result is NotImplemented:
#             return NotImplemented
#         else:
#             return not result
#
#     def __lt__(self, other: ValueObject[T]) -> bool:
#         if other.__class__ is self.__class__:
#             return self.value < typing.cast(ValueObject, other).value
#         else:
#             return NotImplemented
#
#     def __le__(self, other: ValueObject[T]) -> bool:
#         if other.__class__ is self.__class__:
#             return self.value <= typing.cast(ValueObject, other).value
#         else:
#             return NotImplemented
#
#     def __gt__(self, other: ValueObject[T]) -> bool:
#         if other.__class__ is self.__class__:
#             return self.value > typing.cast(ValueObject, other).value
#         else:
#             return NotImplemented
#
#     def __ge__(self, other: ValueObject[T]) -> bool:
#         if other.__class__ is self.__class__:
#             return self.value >= typing.cast(ValueObject, other).value
#         else:
#             return NotImplemented
#
#     def __hash__(self) -> int:
#         return hash(self.value)
#
#     def __repr__(self) -> str:
#         return f"{self.__class__.__name__}({self.value!r})"
#
#     def __str__(self) -> str:
#         return str(self.value)
#
#
# class OpaqueValueObject(ValueObject[T], typing.Generic[T]):
#     def __repr__(self):
#         return f"{self.__class__.__name__}(***)"
#
#     __str__ = __repr__
#
#
# class NonEmptyStr(ValueObject[str]):
#     def __init__(
#         self,
#         /,
#         value: str,
#         *,
#         min_length: int = 1,
#         max_length: typing.Optional[int] = None,
#     ):
#         if not value:
#             raise ValueError("Value is required.")
#         elif len(value) < min_length:
#             raise ValueError(f"Value must be >= {min_length} characters.")
#         elif max_length and len(value) > max_length:
#             raise ValueError(f"Value must be <= {max_length} characters.")
#         else:
#             super().__init__(value)
#
#
# class OpaqueNonEmptyStr(NonEmptyStr):
#     def __repr__(self):
#         return f"{self.__class__.__name__}(***)"
#
#     __str__ = __repr__
#
#
# class PositiveInt(ValueObject[int]):
#     def __init__(self, /, value: int, *, allow_zero: bool = True):
#         if value is None:
#             raise ValueError(f"A {self.__class__.__name__} value cannot be None.")
#         elif value < 0:
#             raise ValueError(f"A {self.__class__.__name__} value cannot be negative.")
#         elif allow_zero is False and value == 0:
#             raise ValueError(f"A {self.__class__.__name__} value must be >= 0.")
#         else:
#             super().__init__(value)
#
#
# class DatabaseName(NonEmptyStr):
#     ...
#
#
# class DatabasePort(PositiveInt):
#     def __init__(self, /, value: int):
#         super().__init__(value, allow_zero=False)
#
#
# class DatabaseServer(NonEmptyStr):
#     ...
#
#
# class DatabaseUsername(NonEmptyStr):
#     ...
#
#
# class DbUrl(ValueObject[str]):
#     def __init__(self, /, value: str):
#         if not value:
#             raise ValueError("A database url cannot be blank.")
#         super().__init__(value)
#
#     @property
#     def value(self) -> T:
#         return self._value
#
#
# class PostgresDbUrl(DbUrl):
#     def __init__(
#         self,
#         *,
#         database: DatabaseName,
#         password: Password,
#         port: DatabasePort,
#         server: DatabaseServer,
#         username: DatabaseUsername,
#     ):
#         con_str = f"postgresql://{username.value}:{password.value}@{server.value}:{port.value}/{database.value}"
#         super().__init__(con_str)
#
#         self._database = database
#         self._password = password
#         self._port = port
#         self._server = server
#         self._username = username
#
#     def __repr__(self) -> str:
#         return (
#             f"{self.__class__.__name__}(database={self._database!r}, password={self._password!r}, port={self._port!r}, "
#             f"server={self._server!r}, username={self._username!r})"
#         )
#
#     __str__ = __repr__
#
#
# class Password(OpaqueNonEmptyStr):
#     def __init__(self, /, value: str):
#         super().__init__(value, min_length=6)
#
#
# class PasswordHash(NonEmptyStr):
#     ...
