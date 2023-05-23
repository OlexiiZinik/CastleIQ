from tortoise.contrib.fastapi import register_tortoise

from api import app
from config import conf
from logger import logger


@app.on_event('startup')
def on_startup():
    logger.info("App started")


def main():
    if not conf.testing:
        register_tortoise(
            app,
            config=conf.tortoise_conf,
            add_exception_handlers=True
        )


if __name__ == "main":
    main()


if __name__ == '__main__':
    logger.critical("Program started as __main__")
    