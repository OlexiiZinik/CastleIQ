from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from castleiq_events.common import Webhook, EventDescription


class Device(Model):
    name = fields.CharField(max_length=200)
    description = fields.CharField(max_length=500)
    room = fields.CharField(max_length=200)

    protocol = fields.CharField(max_length=10, default="http")
    ip = fields.CharField(max_length=15)
    port = fields.IntField()
    path = fields.CharField(max_length=100)

    events: fields.ReverseRelation["DeviceEvent"]

    @property
    def active(self) -> bool:
        return True


class DevicePydantic(BaseModel):
    name: str
    description: str
    room: str
    id: int
    webhook: Webhook
    events: list[EventDescription]


class DeviceEvent(Model):
    device = fields.ForeignKeyField("modules.Device", "events")
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=500)
    outgoing = fields.BooleanField(default=False)
    event_schema = fields.TextField()
