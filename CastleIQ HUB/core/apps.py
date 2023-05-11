import importlib
from fastapi import FastAPI, APIRouter

from logger import logger


def include_apps(server: FastAPI, apps: list[str]):
    for a in apps:
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
                logger.warning(f'App {a} does not contain handlers.py')
                continue

            router = getattr(handlers, "router", None)

            if router is None or type(router) != APIRouter:
                logger.warning(f"App {a} does not have a router in {a}.handlers")
                continue

        server.include_router(router)
        logger.info(f'App {a} included successfully')