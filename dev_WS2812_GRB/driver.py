import os

import uvicorn
from castleiq_events.common import Webhook, EventDescription, get_my_ip

from loader import driver, event_manager, pixels, num_pixels
from events import *

from effects import Effect
from effects.rainbow import RainbowEffect
from effects.single_color import SingleColor
from effects.sliding_rainbow import SlidingRainbowEffect

# todo save to file
CASTLE_IQ_HUB: Webhook | None = None

CURRENT_EFFECT: Effect | None = None

EFFECTS = {
    Modes.SINGLE_COLOR: SingleColor,
    Modes.RAINBOW: RainbowEffect,
    Modes.SLIDING_RAINBOW: SlidingRainbowEffect
}


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
        events=[EventDescription(name=ev["name"], event_schema=ev["event_schema"], outgoing=ev["outgoing"]) for ev in event_manager.get_registered_events()],
        name="WS2812 Lamp",
        description="Розумна лампа на адресованих світлодіодах",
        webhook=Webhook(ip=get_my_ip(), port=8001, path="/fire_event"),
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


@event_manager.on(ShowColorEvent)
def show_color(event: ShowColorEvent):
    global CURRENT_EFFECT
    global EFFECTS
    event = ShowColorEvent(**(event.dict()))
    effect = None
    if event.mode:
        effect = EFFECTS.get(event.mode, None)
    
    if effect:
        if CURRENT_EFFECT:
            CURRENT_EFFECT.stop()
        CURRENT_EFFECT = effect(pixels)

        if event.mode == Modes.SINGLE_COLOR:
            CURRENT_EFFECT.start(event.color)
        else:
            CURRENT_EFFECT.start()
    else:
        return ColorShownEvent(color=Color(R=0,G=0,B=0))

    print(f"showing color ({event.color})")

    return ColorShownEvent(color=Color(R=0,G=0,B=0))


if __name__ == "__main__":
    try:
        uvicorn.run(driver, host="0.0.0.0", port=8001)
    except:
        raise
    finally:
        pixels.deinit()
