from pydantic import BaseModel
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    username = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


UserPydantic = pydantic_model_creator(User, name="User", exclude=("hashed_password",))
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)


class UserCredentials(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
