import pytest
from tortoise.contrib.test import finalizer, initializer
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from config import conf
from logger import logger


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def initialize_db(request):
    logger.disable("api")
    logger.disable("main")
    logger.disable("core")
    initializer([a + '.models' for a in conf.apps] + ["tests.testmodels"], db_url=conf.test_conn_str)
    request.addfinalizer(finalizer)


@pytest.fixture(scope="session")
async def client():
    logger.disable("api")
    logger.disable("core")
    logger.disable("main")
    conf.testing = True
    from main import app
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c
