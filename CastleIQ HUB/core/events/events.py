from enum import Enum
from pydantic import BaseModel


class RaisedEvent(Exception):
    data: "Event"

    def __init__(self, data: "Event"):
        self.data = data
        super(RaisedEvent, self).__init__()


def raise_event(event: "Event"):
    raise RaisedEvent(data=event)


class EventResult(Enum):
    SUCCESS = "Success"
    ERROR = "Error"


class Event(BaseModel):
    status_code: int
    event_result: EventResult
    event_name: str = "Event"
    message: str

    def fire(self):
        raise_event(self)


