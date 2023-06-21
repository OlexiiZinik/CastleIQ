from neopixel import NeoPixel
from threading import Thread, Event
import colorsys


def hsv_to_rgb(h: int, s: int, v: int):
    # normalize
    (h, s, v) = (h / 255, s / 255, v / 179)
    # convert to RGB
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    # expand RGB range
    (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))
    return (r, g, b)


class Effect:
    def __init__(self, pixels: NeoPixel):
        self.running = Event()
        self.pixels = pixels
        self.thread = Thread(target=self.run)

    def start(self, *args):
        self.running.set()
        self.thread = Thread(target=self.run, args=(*args,))
        self.thread.start()

    def stop(self):
        self.running.clear()
        self.thread.join()

    def run(self):
        pass
