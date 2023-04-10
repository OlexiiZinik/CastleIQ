from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator

from tortoise.models import Model
from pydantic import BaseModel
from .models import UserInPydantic, UserPydantic
from logger import logger
