from api.direct_device_api.models import DevicePydantic
from castleiq_events import RequestEvent, ResponseEvent, EventResult
from castleiq_events.common import Webhook, DeviceInfo

from event_manager import event_manager


@event_manager.register_event
class ConnectNewDevice(RequestEvent):
    event_name = "ConnectNewDevice"
    webhook: Webhook
    room: str


class ConnectionFailedError(ResponseEvent):
    event_name = "ConnectionFailedError"
    status_code = 404
    event_result = EventResult.ERROR
    message = "Не вдалось з'єднатись"


class DeviceConnected(ResponseEvent):
    event_name = "DeviceConnected"
    status_code = 200
    event_result = EventResult.SUCCESS
    message = "Пристрій підключено"
    device_info: DeviceInfo


class AllDevices(ResponseEvent):
    event_name = "AllDevices"
    status_code = 200
    event_result = EventResult.SUCCESS
    message = ""
    devices: list[DevicePydantic]
