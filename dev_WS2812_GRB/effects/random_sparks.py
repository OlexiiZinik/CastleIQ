from neopixel import NeoPixel
from random import randint
from . import Effect, hsv_to_rgb
from time import sleep
from typing import Tuple


# def get_neighbours(rows, columns, pix_id):
#     num_pixels = rows * columns

#     pix_row = pix_id % rows
#     pix_col = pix_id % columns

def index_to_coords(index: int, num_rows: int, num_cols: int) -> Tuple[int, int]:
    """
    Translates a linear index to 2D coordinates for a num_rows x num_cols WS2812 LED matrix with a zigzag pattern.

    Args:
        index: The linear index of the LED.
        num_rows: The number of rows in the LED matrix.
        num_cols: The number of columns in the LED matrix.

    Returns:
        A tuple containing the x and y coordinates of the LED.
    """
    if index < 0 or index >= num_rows * num_cols:
        raise ValueError("Invalid LED index")
    x = index % num_cols
    y = index // num_cols
    if y % 2 == 1:
        x = num_cols - 1 - x
    return (x, y)


def coords_to_index(x: int, y: int, num_rows: int, num_cols: int) -> int:
    """
    Translates 2D coordinates to a linear index for a num_rows x num_cols WS2812 LED matrix with a zigzag pattern.

    Args:
        x: The x-coordinate of the LED.
        y: The y-coordinate of the LED.
        num_rows: The number of rows in the LED matrix.
        num_cols: The number of columns in the LED matrix.

    Returns:
        The linear index of the LED.
    """
    if x < 0 or x >= num_cols or y < 0 or y >= num_rows:
        raise ValueError("Invalid LED coordinates")
    if y % 2 == 1:
        x = num_cols - 1 - x
    index = y * num_cols + x
    return index

class RandomEffect(Effect):
    
    def run(self):
        # rows = 11
        # columns = 13
        
        # self.pixels[3] = (255,255,255)
        # self.pixels[12] = (255,255,255)
        
        print(index_to_coords(0, 11, 13))
        for y in range(11):
            for x in range(13):
                index = coords_to_index(x,y,11,13)
                self.pixels.fill((0,0,0))
                self.pixels[index] = (255,255,255)
                self.pixels.show()

        while self.running.is_set():
            sleep(.1)
            # pix = randint(0, len(self.pixels)-1)
            # h, s, v = randint(0, 255), 255, 179
            # self.pixels[pix] = hsv_to_rgb(h, s, v)
            # self.pixels.show()
            # for _ in range(10):
            #     v = v - 179 / 10
            #     self.pixels[pix] = hsv_to_rgb(h, s, v)
            #     self.pixels.show()
            #     sleep(.02)
            # self.pixels.fill((0,0,0))
            # self.pixels.show()

