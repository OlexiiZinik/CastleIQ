import pytest
from tortoise.contrib.test import finalizer, initializer
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from main import app
from config import conf
# @pytest.fixture(scope="session", autouse=True)
# def initialize_tests(request):
#     db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
#     initializer(["tests.testmodels"], db_url=db_url, app_label="tests.testmodels")
#     request.addfinalizer(finalizer)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def initialize_db(request):
    initializer([a + '.models' for a in conf.apps] + ["tests.testmodels"])
    request.addfinalizer(finalizer)


@pytest.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c
