from fastapi import FastAPI, APIRouter
import importlib

from config import conf
from logger import logger


app = FastAPI(
    debug=conf.debug,
    title="CastleIQ HUB",
    description="Smart home server",
    version=conf.version)


@app.get("/")
async def hello_world():
    return {"message": "Hello world"}


# TODO export to core
if __name__ == "api":
    for a in conf.apps:
        try:
            lib = importlib.import_module(a)
        except ModuleNotFoundError:
            logger.warning(f'App {a} does not exist')
            continue

        router = getattr(lib, "router", None)
        if router is None or type(router) != APIRouter:
            logger.debug(f'Router in {a}.__init__ not found')
            logger.debug(f'Importing {a}.handlers')
            try:
                handlers = importlib.import_module(a + '.handlers')
            except ModuleNotFoundError:
                logger.warning(f'App {a} does contain handlers.py')
                continue

            router = getattr(handlers, "router", None)

            if router is None or type(router) != APIRouter:
                logger.warning(f"App {a} does not have a router in {a}.handlers")
                continue

        app.include_router(router)
        logger.info(f'App {a} included successfully')
