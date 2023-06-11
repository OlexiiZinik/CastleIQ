from . import Effect, hsv_to_rgb
from time import sleep

def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0

    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0

    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)

    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)

    return (r, g, b)


class SlidingRainbowEffect(Effect):
    
    def run(self):
        while self.running.is_set():
            for j in range(255):
                for i in range(len(self.pixels)):
                    pixel_index = (i * 256 // len(self.pixels)) + j
                    self.pixels[i] = wheel(pixel_index & 255)
                    if not self.running.is_set():
                        self.pixels.fill((0,0,0))
                        self.pixels.show()
                        return
                self.pixels.show()
                sleep(0.01)

            if not self.running.is_set():
                self.pixels.fill((0,0,0))
                self.pixels.show()
                return
        self.pixels.fill((0,0,0))
        self.pixels.show()

                
