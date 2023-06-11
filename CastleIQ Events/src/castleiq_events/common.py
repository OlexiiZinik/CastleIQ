from pydantic import BaseModel

from castleiq_events import ResponseEvent, RequestEvent, EventResult


class Webhook(BaseModel):
    protocol: str = "http"
    ip: str
    port: int
    path: str = "/fire_event"


class EventDescription(BaseModel):
    name: str
    event_schema: dict


class DeviceInfo(ResponseEvent):
    status_code = 200
    event_result = EventResult.SUCCESS
    event_name = "DeviceInfo"
    name: str
    description: str
    id: int
    webhook: Webhook
    events: list[EventDescription]
    message = ""


class ConnectEvent(RequestEvent):
    event_name = "ConnectEvent"
    id: int
    hub_webhook: Webhook


class ConnectedEvent(ResponseEvent):
    status_code = 200
    event_result = EventResult.SUCCESS
    event_name = "ConnectedEvent"
    device_info: DeviceInfo


class ValidationError(ResponseEvent):
    status_code = 422
    event_name = "ValidationError"
    event_result = EventResult.ERROR
    message = "Не вдалось розпарсити"
