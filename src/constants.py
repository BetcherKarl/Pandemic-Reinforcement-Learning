from PIL import Image
from typing import Tuple
from pygame.surfarray import make_surface
from pygame.transform import rotate
import numpy as np


colors = {"amber": (255, 191, 0),
          "blue": (0, 0, 255),
          "yellow": (255, 255, 0),
          "black": (0, 0, 0),
          "red": (255, 0, 0),
          "green": (0, 255, 0),
          "dark green": (0, 150, 0),
          "purple": (128, 0, 128),
          "orange": (255, 165, 0),
          "white": (255, 255, 255),
          "brown": (165, 42, 42),
          "pink": (255, 192, 203),
          "gray": (128, 128, 128),
          "cyan": (0, 255, 255),
          "magenta": (255, 0, 255),
          "olive": (128, 128, 0),
          "maroon": (128, 0, 0),
          "lime": (50, 200, 50)}

board_size = 0.65

horizontal_card_size = (0.14, 0.14)
vertical_card_size = (0.1, 0.2)

r_seed = 42069

radius = 30

def get_image(path: str, resolution: Tuple[int, int]) -> Image:
    img = Image.open(path)
    img = img.resize(resolution)
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img = make_surface(np.array(img))
    img = rotate(img, 270)
    return img
