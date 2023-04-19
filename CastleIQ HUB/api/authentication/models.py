from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
