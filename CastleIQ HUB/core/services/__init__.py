from abc import ABC
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise.queryset import QuerySet, QuerySetSingle
from pydantic import BaseModel
from logger import logger


# Абстрактний клас Service
class Service(ABC):
    pass


class ModelService(Service):
    model: type[Model] = None
    pydantic_model_in: type[BaseModel] = None
    pydantic_model_out: type[BaseModel] = None

    def __init__(
            self,
            model: type[Model] | None = None,
            pydantic_model_in: type[BaseModel] | None = None,
            pydantic_model_out: type[BaseModel] | None = None,
    ) -> None:
        if self.model is None and model is not None:
            self.model = model
        elif self.model is None and model is None:
            raise ValueError(f"Model cannot be None")

        if self.pydantic_model_in is None and pydantic_model_in is not None:
            self.pydantic_model_in = pydantic_model_in

        if self.pydantic_model_out is None and pydantic_model_out is not None:
            self.pydantic_model_out = pydantic_model_out

    def get_model(self) -> type[Model]:
        return self.model

    @property
    def model_name(self) -> str:
        return self.get_model().__name__

    def get_pydantic_model_in(self) -> type[BaseModel]:
        if self.pydantic_model_in is None:
            self.pydantic_model_in = pydantic_model_creator(
                self.get_model(),
                name=f"{self.model_name}In",
                exclude_readonly=True
            )
        return self.pydantic_model_in

    def get_pydantic_model_out(self) -> type[BaseModel]:
        if self.pydantic_model_out is None:
            self.pydantic_model_out = pydantic_model_creator(
                self.get_model(),
                name=f"{self.model_name}"
            )
        return self.pydantic_model_out

    @property
    def pmi(self) -> type[BaseModel]:
        return self.get_pydantic_model_in()

    @property
    def pmo(self) -> type[BaseModel]:
        return self.get_pydantic_model_in()

    def _raise_if_object_types_dont_match(self, obj: any, t: type):
        if type(obj) != t:
            raise TypeError(f"Object {obj} type {type(obj)} does not match with {t}")

    async def api_create_object(self, obj: BaseModel) -> Model:
        self._raise_if_object_types_dont_match(obj, self.get_pydantic_model_in())

        obj = await self.get_model().create(**obj.dict(exclude_unset=True))
        await obj.save()
        return obj

    async def api_get_object(self, pk: int) -> Model:
        obj = await self.get_model().get(pk=pk)
        return obj

    async def api_get_multiple(
            self,
            offset: int | None = None,
            limit: int | None = None,
    ) -> list[Model]:
        if offset is None:
            offset = 0

        if limit is None:
            limit = 1_000_000

        objects = await self.get_model().all().offset(offset).limit(limit).all()
        return objects

    async def api_get_all(self) -> list[Model]:
        objects = await self.get_model().all()
        return objects

    async def api_update_object(self, pk: int, new_obj: BaseModel) -> Model:
        self._raise_if_object_types_dont_match(new_obj, self.get_pydantic_model_in())
        obj = await self.api_get_object(pk)
        obj = await obj.update_from_dict(new_obj.dict(exclude_unset=True))
        return obj

    async def api_delete_object(self, pk: int) -> None:
        obj = await self.api_get_object(pk)
        await obj.delete()
