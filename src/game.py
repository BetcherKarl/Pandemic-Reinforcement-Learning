from utils.board import PandemicBoard
from utils.card import Card
from constants import board_size, r_seed

from PIL import Image
import numpy as np
import pygame as pg

import json
from threading import Thread
from time import sleep
import random
from typing import Tuple

random.seed(r_seed)

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
background_resolution = (int(board_size * resolution[0]), int(board_size * resolution[1]))
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

loc = (1 - board_size) / 2
background_top = int(loc * resolution[0])
background_left = int(loc * resolution[1])
last_res = resolution
# initialize the Pandemic board

# get the background and resize it
table = get_image('assets/wood_texture.jpg', resolution)
background = get_image('assets/pandemic_game_board.jpg', background_resolution)

board: PandemicBoard
board = PandemicBoard(screen, num_players=4, seed=r_seed)

running = True


# function to test behavior of code
def wait_test(wait_time=4):
    global board
    print("Running a small test case")
    for i in range(8):
        sleep(wait_time)
        board.current_player.save_the_day()
        sleep(wait_time / 2)
        board.next_player()


testing_thread = Thread(target=wait_test)
testing_thread.start()
# str4tttttttttttttttttttttttttttttttttttett5t - Merlin (my cat)

for player in board.players:
    print(f"Player {player.role}")
    for card in player.hand:
        print(f"{card.color} ({card.name})")
    print()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # display the background (resize if not the same size as last frame)
    resolution = screen.get_size()
    if resolution != last_res:
        background_resolution = (int(board_size * resolution[0]), int(board_size * resolution[1]))
        print(f"Resolution: {resolution}")
        print(f"Background resolution: {background_resolution}")
        background = get_image('assets/pandemic_game_board.jpg', background_resolution)
        background_top = int(loc * resolution[0])
        background_left = int(loc * resolution[1])
        table = get_image('assets/wood_texture.jpg', resolution)
        last_res = resolution
    screen.blit(table, (0, 0))
    screen.blit(background, (background_top, background_left))

    # TODO: Click to view cards in discards
    board.draw()

    pg.display.update()

    if len(board._player_deck) == 58 - len(board.players) * (6 - len(board.players)) - 16:
        print("Test case finished successfully")
        break

print("Game Over")