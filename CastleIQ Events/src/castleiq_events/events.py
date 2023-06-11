from enum import Enum

import pydantic
from pydantic import BaseModel


class RaisedEvent(Exception):
    data: "ResponseEvent"

    def __init__(self, data: "ResponseEvent"):
        self.data = data
        super(RaisedEvent, self).__init__()


def raise_event(event: "ResponseEvent"):
    raise RaisedEvent(data=event)


class EventResult(Enum):
    SUCCESS = "Success"
    ERROR = "Error"


class Event(BaseModel):
    event_name: str = "Event"
    event_type: str

    class Config:
        allow_population_by_field_name = True
        extra = pydantic.Extra.allow


class RequestEvent(Event):
    event_type: str = "RequestEvent"
    pass


class ResponseEvent(Event):
    event_type: str = "ResponseEvent"
    status_code: int
    event_result: EventResult
    message: str

    def fire(self):
        raise_event(self)


class Direction(Enum):
    TO_DEVICE = "To device"
    TO_UI = "To UI"


class ForwardEvent(RequestEvent):
    event_name = "ForwardEvent"
    direction: Direction
    device_id: int
    event: dict
