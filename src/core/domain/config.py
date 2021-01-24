import pydantic

__all__ = ("Config",)

#  To generate a secret_key run the following command: openssl rand -hex 32


class Config(pydantic.BaseSettings):
    db_url: pydantic.AnyUrl
    secret_key: pydantic.SecretStr
    access_token_expire_minutes: pydantic.PositiveInt
    hashing_algorithm: str
