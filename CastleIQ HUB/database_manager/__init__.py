from tortoise.contrib.fastapi import register_tortoise
from config import conf
from api import app


TORTOISE_ORM = {
    "connections": {
        "default": conf.db_conn_str,
    },
    "apps": {
        "modules": {
            "models": [a + '.models' for a in conf.apps] + ["aerich.models"],
            "default_connection": "default",
        },
    },
    "add_exception_handlers":True
}


register_tortoise(
    app,
    config=TORTOISE_ORM,
    add_exception_handlers=True
)


# register_tortoise(
#     app,
#     db_url=conf.db_conn_str,
#     modules={"models": [a + '.models' for a in conf.apps]},
#     generate_schemas=True,
#     add_exception_handlers=True
# )