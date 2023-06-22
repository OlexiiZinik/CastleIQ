import asyncio


from api import app
from api.authentication.models import User
from api.automations.handlers import subscribe_on_startup
from api.automations.models import Automation
from config import conf
from logger import logger
from tortoise.contrib.fastapi import register_tortoise


@app.on_event('startup')
async def on_startup():
    logger.info("App started")
    #await subscribe_on_startup()
    #print(await User.all())



def main():
    if not conf.testing:
        register_tortoise(
            app,
            config=conf.tortoise_conf,
            add_exception_handlers=True
        )
        logger.info("Db inited")

    subscribe_on_startup()


if __name__ == "main":
    main()

if __name__ == '__main__':
    logger.critical("Program started as __main__")
