import os

from pydantic import BaseSettings


class Config(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    reload: bool = True
    testing: bool = False
    version: str = "0.1.2"
    log_level: str = "INFO"
    db_conn_str: str = "sqlite:///./db.sqlite"
    test_conn_str: str = "sqlite://:memory:"
    apps: list[str] = [
        "api.direct_device_api",
        "api.ui_api",
        "api.authentication"
    ]
    # Dummy secret key (used for testing) DO NOT USE IT IN PRODUCTION! Run $ openssl rand -hex 32 to generate new one
    secret_key: str = "4c93bbc6b1266ed337b6e3571ab5868134c230a13741479028cafa284888c14c"
    timezone: str = "Europe/Kyiv"
    algorithm: str = "HS256"
    token_expire_minutes: int = 60

    @property
    def tortoise_conf(self):
        return {
            "connections": {
                "default": self.db_conn_str,

            },
            "apps": {
                "modules": {
                    "models": [a + '.models' for a in self.apps] + ["aerich.models"],
                    "default_connection": "default",
                },
            },
            "add_exception_handlers": True
        }


conf = Config(
    _env_file=".env",
    _env_file_encoding="utf-8"
)
TORTOISE_CONFIG = conf.tortoise_conf
