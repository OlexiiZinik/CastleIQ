import json

import pydantic
from fastapi import Depends
from fastapi.routing import APIRouter
import httpx
from tortoise.exceptions import DoesNotExist

from castleiq_events.common import ConnectEvent, DeviceInfo, Webhook, EventDescription
from castleiq_events import RequestEvent
import socket

from castleiq_events.events import ForwardEvent, Direction
from .models import Device, DeviceEvent, DevicePydantic
from config import conf
from .events import ConnectNewDevice, ConnectionFailedError, DeviceConnected, AllDevices
from logger import logger
from event_manager import event_manager
from api.authentication.services import UserService
from ..authentication.models import User

user_service = UserService()

router = APIRouter(prefix="/dev_api", tags=["DeviceAPI"])


@router.post("/connect_new", response_model=DeviceConnected)
async def connect_new_device(connect_new_device_event: ConnectNewDevice,
                             user: User = Depends(user_service.get_current_user)):
    logger.info(connect_new_device_event)

    async with httpx.AsyncClient() as client:
        # Get info about device
        print(f'{connect_new_device_event.webhook.protocol}://{connect_new_device_event.webhook.ip}:{connect_new_device_event.webhook.port}/get_info')
        try:
            response = await client.get(
                f'{connect_new_device_event.webhook.protocol}://{connect_new_device_event.webhook.ip}:{connect_new_device_event.webhook.port}/get_info')

            device_info = DeviceInfo.parse_raw(response.text)
            if device_info.id not in [None, "", 0, "0"]:
                try:
                    device = await Device.get(id=device_info.id)
                    await device.events.all().delete()
                    await device.save()
                    for device_event in device_info.events:
                        de = await DeviceEvent.create(
                            device=device,
                            name=device_event.name,
                            description="",
                            event_schema=device_event.event_schema
                        )
                        await de.save()
                    DeviceConnected(message="Пристрій вже під'єднано", device_info=device_info).fire()
                except DoesNotExist:
                    pass

        except httpx.ConnectError:
            ConnectionFailedError(message="Не вдалось отримати інформацію про пристрій").fire()

        except pydantic.ValidationError:
            ConnectionFailedError(staus_code=500, message="Щось пішло не так. Не вдалось розпарсити DeviceInfo").fire()
        else:
            db_device = Device()
            db_device.name = device_info.name
            db_device.description = device_info.description
            db_device.ip = device_info.webhook.ip
            db_device.port = device_info.webhook.port
            db_device.path = device_info.webhook.path
            db_device.room = connect_new_device_event.room
            await db_device.save()
            for device_event in device_info.events:
                de = await DeviceEvent.create(
                    device=db_device,
                    name=device_event.name,
                    description="",
                    event_schema=device_event.event_schema,
                )
                await de.save()

            try:
                connect_event = ConnectEvent(
                    hub_webhook=Webhook(ip=socket.gethostbyname(socket.gethostname()), port=conf.port,
                                        path="/dev_api/fire_event"), id=db_device.pk)

                response = await client.post(
                    f'{connect_new_device_event.webhook.protocol}://{connect_new_device_event.webhook.ip}:{connect_new_device_event.webhook.port}{connect_new_device_event.webhook.path}',
                    content=connect_event.json())
                device_info = DeviceInfo.parse_raw(response.text)
                print(device_info)
                assert device_info.id == db_device.pk
                return DeviceConnected(device_info=device_info)

            except httpx.ConnectError:
                ConnectionFailedError().fire()
            except AssertionError:
                ConnectionFailedError(staus_code=500, message="Щось пішло не так").fire()


@router.get("/devices", response_model=AllDevices)
async def all_devices(user: User = Depends(user_service.get_current_user)):
    devices = await Device.all().prefetch_related("events")
    devices_pydantic = AllDevices(devices=[])
    for dev in devices:
        dev_pydantic = DevicePydantic(
            name=dev.name,
            description=dev.description,
            events=[EventDescription(name=ev.name, event_schema=json.loads(str(ev.event_schema).replace("'", '"'))) for
                    ev in dev.events],
            id=dev.pk,
            webhook=Webhook(protocol=dev.protocol, ip=dev.ip, port=dev.port, path=dev.path),
            room=dev.room
        )
        devices_pydantic.devices.append(dev_pydantic)

    return devices_pydantic


@router.post("/fire_event")
async def fire_event(event: RequestEvent):
    logger.info(event)
    result = await event_manager.fire(event)
    if result:
        result = list(filter(lambda x: x is not None, result))
        return result[0] if len(result) > 0 else None


@event_manager.on(ForwardEvent)
async def forward_to_device(event: ForwardEvent):
    if event.direction != Direction.TO_DEVICE:
        return

    try:
        device = await Device.get(pk=event.device_id)
    except DoesNotExist:
        ConnectionFailedError(message="Пристрій не знайдено").fire()
        return
    logger.debug(f"Connecting to{device.protocol}://{device.ip}:{device.port}{device.path}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'{device.protocol}://{device.ip}:{device.port}{device.path}',
                content=json.dumps(event.event))
            logger.debug(response)
            logger.debug(response.text)
            return json.loads(response.text)
    except httpx.ConnectError:
        ConnectionFailedError().fire()
