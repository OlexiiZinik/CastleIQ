import asyncio
import pytest
from tortoise.contrib.test import finalizer, initializer
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError, OperationalError, DoesNotExist
from pydantic import BaseModel

from core.services import ModelService
from .testmodels import ExampleModel, ExamplePydantyc


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module", autouse=True)
def initialize_db(request):
    initializer(["tests.testmodels"])
    request.addfinalizer(finalizer)


@pytest.fixture
def ms():
    yield ModelService(ExampleModel)


@pytest.fixture(autouse=True)
def drop_db(ms):
    async def _drop_db():
        try:
            await ExampleModel.all().delete()
        except (DBConnectionError, OperationalError):
            pass
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_drop_db())


def test_empty_constructor_as_instance():
    with pytest.raises(ValueError):
        ms = ModelService()


def test_empty_constructor_as_inherited():
    class MyModelService(ModelService):
        pass

    with pytest.raises(ValueError):
        ms = MyModelService()

@pytest.mark.anyio
async def test_creation(ms: ModelService):
    obj = await ms.api_create_object(ms.pmi(name="Hello", password="World"))
    assert obj.pk != None


@pytest.mark.anyio
async def test_creation_arguments(ms: ModelService):
    class ExamplePy(BaseModel):
        field1: str
        field2: str

    example_data = ExamplePy(field1="123", field2="456")
    with pytest.raises(TypeError):
        obj = await ms.api_create_object(example_data)

@pytest.mark.anyio
async def test_creation_arguments_same_dataclass(ms: ModelService):
    class MyModelService(ModelService):
        model = ExampleModel
        pydantic_model_in = ExamplePydantyc
    ms1 = MyModelService()
    example_data = ExamplePydantyc(name="123", password="456")
    obj = await ms1.api_create_object(example_data)
    assert obj.pk != None


@pytest.mark.anyio
async def test_get_object(ms: ModelService):
    obj = await ms.api_create_object(ms.pmi(name="Hello", password="World"))
    assert obj.pk != None
    obj_from_db = await ms.api_get_object(obj.pk)
    assert obj == obj_from_db

@pytest.mark.anyio
async def test_get_object_does_not_exist(ms: ModelService):
    with pytest.raises(DoesNotExist):
        obj_from_db = await ms.api_get_object(1)
    

@pytest.mark.anyio
async def test_get_multiple(ms: ModelService):
    for i in range(10):
        await ms.api_create_object(ms.pmi(name=f"name {i}", password=f"password {i}"))

    objects = await ms.api_get_multiple()
    assert len(objects) == 10


@pytest.mark.anyio
async def test_get_multiple_with_params(ms: ModelService):
    for i in range(10):
        await ms.api_create_object(ms.pmi(name=f"name {i}", password=f"password {i}"))

    objects = await ms.api_get_multiple(offset=1, limit=3)
    assert len(objects) == 3


@pytest.mark.anyio
async def test_get_all(ms: ModelService):
    for i in range(10):
        await ms.api_create_object(ms.pmi(name=f"name {i}", password=f"password {i}"))

    objects = await ms.api_get_all()
    assert len(objects) == 10


@pytest.mark.anyio
async def test_update(ms: ModelService):
    obj = await ms.api_create_object(ms.pmi(name=f"name 1", password=f"password 1"))

    upd_obj = await ms.api_update_object(obj.pk, ms.pmi(name="name 1 updated", password="password 1 updated"))

    assert upd_obj.pk == obj.pk
    assert upd_obj.name == "name 1 updated"
    assert upd_obj.password == "password 1 updated"

@pytest.mark.anyio
async def test_update_not_existing(ms: ModelService):
    with pytest.raises(DoesNotExist):
        upd_obj = await ms.api_update_object(1_000_000, ms.pmi(name="name 1 updated", password="password 1 updated"))


@pytest.mark.anyio
async def test_delete(ms: ModelService):
    obj = await ms.api_create_object(ms.pmi(name=f"name 1", password=f"password 1"))
    
    assert await ExampleModel.all().count() == 1

    await ms.api_delete_object(obj.pk)
    
    assert await ExampleModel.all().count() == 0


@pytest.mark.anyio
async def test_delete_not_existing(ms: ModelService):
    with pytest.raises(DoesNotExist):
        upd_obj = await ms.api_delete_object(1_000_000)

