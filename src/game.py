from utils.board import PandemicBoard

from PIL import Image
import numpy as np
import pygame as pg

import json
from threading import Thread
from time import sleep
import random
from typing import Tuple

def get_image(path: str, resolution: Tuple[int, int]) -> Image:
    img = Image.open(path)
    img = img.resize(resolution)
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img = pg.surfarray.make_surface(np.array(img))
    img = pg.transform.rotate(img, 270)
    return img


# import preferences
pg_settings = json.load(open("configs/pygame.json", "r"))
resolution = (pg_settings["resolution"][0], pg_settings["resolution"][1])
background_resolution = (int(0.75 * resolution[0]), int(0.75 * resolution[1]))
print(f"Resolution: {resolution}")
print(f"Background resolution: {background_resolution}")

# Initialize the game
if pg_settings["display"] == "windowed":
    screen = pg.display.set_mode(resolution, pg.RESIZABLE)
elif pg_settings["display"] == "fullscreen":
    screen = pg.display.set_mode(resolution, pg.FULLSCREEN)
else:
    raise Warning("Invalid display mode. Must be 'windowed' or 'fullscreen'.")

pg.init()
pg.display.set_caption(pg_settings["title"] + " - " + pg_settings["version"])
print(resolution)
pg.init()


background_top = int(0.125 * resolution[0])
background_left = int(0.125 * resolution[1])
last_res = resolution
# initialize the Pandemic board

# get the background and resize it
table = get_image('assets/wood_texture.jpg', resolution)
background = get_image('assets/pandemic_game_board.jpg', background_resolution)

board = PandemicBoard(screen)

running = True

# function to test behavior of code
def wait_test(wait_time=5):
    global board
    print("Changing infection rate...")

    board.current_player.save_the_day()

testing_thread = Thread(target=wait_test)
# testing_thread.start()
# str4tttttttttttttttttttttttttttttttttttett5t - Merlin (my cat)
print(len(board._player_deck))
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # display the background (resize if not the same size as last frame)
    resolution = screen.get_size()
    if resolution != last_res:
        background_resolution = (int(0.75 * resolution[0]), int(0.75 * resolution[1]))
        print(f"Resolution: {resolution}")
        print(f"Background resolution: {background_resolution}")
        background = get_image('assets/pandemic_game_board.jpg', background_resolution)
        background_top = int(0.125 * resolution[0])
        background_left = int(0.125 * resolution[1])
        table = get_image('assets/wood_texture.jpg', resolution)
        last_res = resolution
    screen.blit(table, (0, 0))
    screen.blit(background, (background_top, background_left))

    # TODO: Click to view cards in discards
    board.draw()

    pg.display.update()

print("Game Over")