from . import Effect, hsv_to_rgb
from time import sleep


class RainbowEffect(Effect):
    def run(self):
        offset = 0
        self.pixels.fill((255, 0, 255))  # hsv_to_rgb(200, 255, 179))
        self.pixels.show()
        while self.running.is_set():
            for i in range(len(self.pixels)):
                self.pixels[i] = hsv_to_rgb(offset, 255, 179)
                self.pixels.show()
                offset += 1
                sleep(0.1)
                if not self.running.is_set():
                    self.pixels.fill((0, 0, 0))
                    self.pixels.show()
                    return
                if offset >= 255:
                    offset = 0

        self.pixels.fill((0, 0, 0))
        self.pixels.show()
