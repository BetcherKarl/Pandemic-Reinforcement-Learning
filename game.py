import pygame as pg
import json
# from utils.board import PandemicBoard


# import preferences
pg_settings = json.load(open("configs/pygame.json", "r"))

# Initialize the game
if pg_settings["display"] == "windowed":
    display_mode = pg.RESIZABLE
elif pg_settings["display"] == "fullscreen":
    display_mode = pg.FULLSCREEN
else:
    raise Warning("Invalid display mode. Must be 'windowed' or 'fullscreen'.")
    display = pg.RESIZABLE

resolution = (pg_settings["resolution"][0], pg_settings["resolution"][1])
pg.init()
pg.display.set_caption(pg_settings["title"] + " - " + pg_settings["version"])
print(resolution)
print(display_mode == pg.RESIZABLE)
screen = pg.display.set_mode(resolution, pg.FULLSCREEN)
background = pg.image.load("assets/pandemic_board.png")
# initialize the Pandemic board
# board = PandemicBoard()

running = True



colors = {"blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "purple": (128, 0, 128),
        "orange": (255, 165, 0),\
        "white": (255, 255, 255),
        "brown": (165, 42, 42),
        "pink": (255, 192, 203),
        "gray": (128, 128, 128),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "olive": (128, 128, 0),
        "maroon": (128, 0, 0)}

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.blit(background, (0, 0))
    

    pg.display.update()


print("Game Over")