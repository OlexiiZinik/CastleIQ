import json

import pydantic
from fastapi import Depends
from fastapi.routing import APIRouter
import httpx
from tortoise.exceptions import DoesNotExist

from castleiq_events.common import ConnectEvent, DeviceInfo, Webhook, EventDescription
from castleiq_events import RequestEvent
import socket
import asyncio
from castleiq_events.events import ForwardEvent, Direction, ResponseEvent, EventResult
from .models import Automation, AutomationPydantic
from config import conf
from .events import AllAutomations
from logger import logger
from event_manager import event_manager
from api.authentication.services import UserService
from .services import AutomationsService
from ..authentication.models import User
from ..direct_device_api.models import DeviceEvent

user_service = UserService()

router = APIRouter(prefix="/automations", tags=["Automations"])

auth_service = UserService()
automations_service = AutomationsService()


def subscribe_on_startup(automations=Depends(automations_service.all)):
    # automations = await automations_service.all()
    # loop = asyncio.get_running_loop()
    # automations = loop.run_until_complete(automations_service.all())
    # logger.debug("Automations initialized")
    # for automation in automations.automations:
    #     event_manager.add_automation(automation.subscribed_on, automation.code)
    pass


@router.get("/all", response_model=AllAutomations)
def all_automations(user: User = Depends(auth_service.get_current_user), automations=Depends(automations_service.all)):
    return automations


@router.post("/create")
async def create_automation(user: User = Depends(auth_service.get_current_user),
                            automation=Depends(automations_service.create)):
    event_manager.add_automation(automation.automation.subscribed_on, automation.automation.code)
    return await automations_service.all()


@router.get("/update")
async def update_automations(user: User = Depends(auth_service.get_current_user)):
    for ev in await DeviceEvent.all():
        try:
            event_manager.register_event(None, ev.name)
        except ValueError:
            pass
    for automation in await Automation.all():
        event_manager.add_automation(automation.subscribed_on, automation.code)

    return ResponseEvent(event_result=EventResult.SUCCESS, status_code=200, message="Події оновлено",
                         event_name="AutomationsUpdated")
