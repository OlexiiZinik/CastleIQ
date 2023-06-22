from enum import Enum

from pydantic import BaseModel
from castleiq_events import ResponseEvent, RequestEvent, EventResult
from castleiq_events.common import DeviceInfo, ConnectEvent

from loader import event_manager


@event_manager.register_ingoing_event
class ChangeStateEvent(RequestEvent):
    event_name = "ChangeStateEvent"
    state: bool


@event_manager.register_outgoing_event
class StateChangedEvent(ResponseEvent):
    event_name = "StateChangedEvent"
    status_code = 200
    event_result = EventResult.SUCCESS
    state: bool
    message = "Стан змінено"


try:
    event_manager.register_event(DeviceInfo)
    event_manager.register_event(ConnectEvent)
except ValueError:
    pass
