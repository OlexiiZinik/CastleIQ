from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel

class ExampleModel(Model):
    name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=100)

    def __repr__(self):
        return f"ExampleModel({self.name=},{self.password=})"

class ExamplePydantyc(BaseModel):
        name: str
        password: str