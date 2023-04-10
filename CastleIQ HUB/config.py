from pydantic import BaseSettings


class Config(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    reload: bool = True
    version: str = "0.1.2"
    log_level: str = "INFO"
    db_conn_str: str = "sqlite:///./db.sqlite"
    apps: list[str] = [
        "api.direct_device_api",
        "api.ui_api",
        "api.authentication"
    ]
    secret_key: str
    timezone: str = "Europe/Kyiv"
    algorithm: str = "HS256"


conf = Config(
    _env_file=".env",
    _env_file_encoding="utf-8"
)