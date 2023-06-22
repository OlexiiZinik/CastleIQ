from pydantic import BaseModel
import socket

from castleiq_events import ResponseEvent, RequestEvent, EventResult

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

class Webhook(BaseModel):
    protocol: str = "http"
    ip: str
    port: int
    path: str = "/fire_event"


class EventDescription(BaseModel):
    outgoing: bool = False
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
