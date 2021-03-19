import typing

import sqlalchemy as sa


def dto_to_dict(obj) -> typing.Dict[str, typing.Any]:  # type: ignore
    return {key: attr.value for key, attr in sorted(sa.inspect(obj).attrs.items())}
