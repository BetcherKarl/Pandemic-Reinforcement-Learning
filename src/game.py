import pygame as pg
import json
import numpy as np
from utils.board import PandemicBoard
from PIL import Image

from constants import colors

# TODO: implement scaling of board for different resolutions

# import preferences
pg_settings = json.load(open("configs/pygame.json", "r"))

resolution = (pg_settings["resolution"][0], pg_settings["resolution"][1])
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

# get the background and resize it
im = Image.open("assets/pandemic_game_board.jpg")
im = im.resize(resolution)
im = im.transpose(Image.FLIP_LEFT_RIGHT)
image_array = np.array(im)
pygame_image = pg.surfarray.make_surface(image_array)
background = pg.transform.rotate(pygame_image, 270)
background_top = 0
background_left = 0
last_res = resolution
# initialize the Pandemic board
board = PandemicBoard(screen)

for _ in range(2):
    board.player_discard.append(board._player_deck.pop())

running = True



while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # display the background
    resolution = screen.get_size()
    if resolution != last_res:
        im = im.resize(resolution)
        # im = im.transpose(Image.FLIP_LEFT_RIGHT)
        image_array = np.array(im)
        pygame_image = pg.surfarray.make_surface(image_array)
        background = pg.transform.rotate(pygame_image, 270)
    last_res = resolution
    screen.blit(background, (background_top, background_left))

    # TODO: cure tracker

    # TODO: outbreak tracker

    # TODO: Turn remaining counter

    # TODO: Player Card Deck/tracker

    # TODO: Click to view cards in discards
    board.draw()

    pg.display.update()

print("Game Over")