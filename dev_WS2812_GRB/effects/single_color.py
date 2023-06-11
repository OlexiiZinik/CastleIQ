from . import Effect, hsv_to_rgb
from time import sleep
from events import Color



class SingleColor(Effect):    
    def run(self, color: Color | None = None):
        if color is None:
            color = Color(R=255, G=255, B=255)
        
        self.pixels.fill((color.R,color.G,color.B))
        self.pixels.show()
        while True:
            if not self.running.is_set():
                self.pixels.fill((0,0,0))
                self.pixels.show()
                break
                
