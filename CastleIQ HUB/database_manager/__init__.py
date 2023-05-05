from tortoise.contrib.fastapi import register_tortoise
from config import conf


def init_db(app):
    register_tortoise(
        app,
        config=conf.tortoise_conf,
        add_exception_handlers=True
    )
