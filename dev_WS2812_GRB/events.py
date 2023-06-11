from enum import Enum

from pydantic import BaseModel
from castleiq_events import ResponseEvent, RequestEvent, EventResult
from castleiq_events.common import DeviceInfo, ConnectEvent

from loader import event_manager


class Color(BaseModel):
    R: int
    G: int
    B: int


class Modes(Enum):
    SINGLE_COLOR = "Single color"
    RAINBOW = "Raibow"
    SLIDING_RAINBOW = "Sliding rainbow"


@event_manager.register_ingoing_event
class ShowColorEvent(RequestEvent):
    event_name = "ShowColorEvent"
    mode: Modes | None
    color: Color | None


@event_manager.register_event
class ColorShownEvent(ResponseEvent):
    status_code = 200
    event_result = EventResult.SUCCESS
    event_name = "ColorShownEvent"
    message = "Колір Показано"
    color: Color


try:
    event_manager.register_event(DeviceInfo)
    event_manager.register_event(ConnectEvent)
except ValueError:
    pass
