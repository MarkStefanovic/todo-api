from src import core


def test_config_hides_secrets() -> None:
    cfg = core.adapter.EnvironConfig()
    assert str(cfg.secret_key) == "1234567890"
    assert repr(cfg) == (
        "EnvironConfig(db_url=pydantic.SecretStr(...), "
        "secret_key=pydantic.SecretKey(...), access_token_expire_minutes=60, "
        "hashing_algorithm='HS256')"
    )
    assert repr(cfg) == str(cfg)
    assert "this is a test" not in str(cfg)
    assert "this is a test" not in repr(cfg)
