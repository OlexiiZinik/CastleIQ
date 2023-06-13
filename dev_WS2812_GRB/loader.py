from fastapi import FastAPI
from castleiq_events import EventManager
import board
import neopixel


pixel_pin = board.D18
num_pixels = 143
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(

    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER

)

event_manager = EventManager()
driver = FastAPI()
