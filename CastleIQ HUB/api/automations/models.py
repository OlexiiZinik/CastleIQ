from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from castleiq_events.common import Webhook, EventDescription


class Automation(Model):
    name = fields.CharField(max_length=200)
    description = fields.CharField(max_length=500)
    subscribed_on = fields.CharField(max_length=200)
    code = fields.TextField()


class AutomationPydantic(BaseModel):
    name: str
    description: str
    subscribed_on: str
    code: str
