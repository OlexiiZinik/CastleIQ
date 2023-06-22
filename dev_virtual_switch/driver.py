import os

import uvicorn

from castleiq_events.common import Webhook, EventDescription, get_my_ip

from loader import driver, event_manager
from events import *

CASTLE_IQ_HUB: Webhook | None = None
STATE: bool = False


def set_my_id(my_id: int):
    with open("device_id.txt", "w") as file:
        file.write(str(my_id))


def get_my_id():
    if not os.path.isfile("device_id.txt"):
        return 0
    with open("device_id.txt", "r") as file:
        my_id = file.readline()
        return int(my_id)


@driver.get("/get_info")
def get_device():
    device = DeviceInfo(
        events=[EventDescription(name=ev["name"], event_schema=ev["event_schema"], outgoing=ev["outgoing"]) for ev in
                event_manager.get_registered_events()],
        name="Віртуальний перемикач",
        description="Віртуальний перемикач",
        webhook=Webhook(ip=get_my_ip(), port=8002, path="/fire_event"),
        id=get_my_id()
    )
    return device


@driver.post("/fire_event")
async def web_hook(event: RequestEvent):
    res = await event_manager.fire(event)
    if res:
        return res[0]


@event_manager.on(ConnectEvent)
def connect(event: ConnectEvent):
    global CASTLE_IQ_HUB
    CASTLE_IQ_HUB = event.hub_webhook
    set_my_id(event.id)
    return get_device()


@event_manager.on(ChangeStateEvent)
def change_state(event: ChangeStateEvent):
    global STATE
    STATE = event.state
    return StateChangedEvent(state=STATE)


if __name__ == "__main__":
    uvicorn.run(driver, host="0.0.0.0", port=8002)
