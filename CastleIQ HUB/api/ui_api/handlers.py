import json

import pydantic
from fastapi import Depends
from fastapi.routing import APIRouter, WebSocket
import httpx
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist

from castleiq_events.common import ValidationError as ValidationErrorEvent
from castleiq_events import RequestEvent

from castleiq_events.events import ForwardEvent, Direction
from logger import logger
from event_manager import event_manager
from api.authentication.services import UserService
from ..authentication.models import User

user_service = UserService()

router = APIRouter(prefix="/ui_api", tags=["UiAPI"])


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#
#     @event_manager.on(ForwardEvent)
#     async def forward(event: ForwardEvent):
#         if event.direction != Direction.TO_UI:
#             return
#         await websocket.send_json(event)
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


@router.post("/fire_event")
async def fire_event(event: RequestEvent, user: User = Depends(user_service.get_current_user)):
    logger.info(event)
    try:
        result = await event_manager.fire(event)
    except ValidationError as ve:
        ValidationErrorEvent(message=f"Помилка валідації{ve.json()}").fire()
        return

    if result:
        result = list(filter(lambda x: x is not None, result))
        return result[0] if len(result) > 0 else None


@event_manager.on(ForwardEvent)
def forward_to_device(event: ForwardEvent):
    if event.direction != Direction.TO_UI:
        return
    print("event to ui", event)
