import pygame as pg
import json
from utils.board import PandemicBoard


# import preferences
pg_settings = json.load(open("configs/pygame.json", "r"))

resolution = (pg_settings["resolution"][0], pg_settings["resolution"][1])
# screen = pg.display.set_mode(resolution, pg.RESIZABLE, 32)
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
background = pg.image.load("assets/pandemic_game_board.jpg")
background_top = 0
background_left = 0
# initialize the Pandemic board
board = PandemicBoard()

running = True



colors = {"blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
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

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # display the background
    screen.blit(background, (background_top, background_left))

    # TODO: cure tracker

    # TODO: outbreak tracker

    # TODO: Infection rate tracker

    # TODO: Turn remaining counter


    # display all cities on the board
    radius = pg_settings["city_circle_radius"]
    for city_name, city in board.cities.items():
        # horizontal, vertical
        # left-right, top-down
        location = [int(city.position[0] * background.get_width()), int(city.position[1] * background.get_height())]

        # display a white outline if the city has a research station
        if city.has_research_station:
            pg.draw.circle(screen, (255, 255, 255), (location[0], location[1]), int(radius * 1.1) + 1)

        # display the city as a circle
        pg.draw.circle(screen, colors[city.color.name], (location[0], location[1]), radius)

        stride = 20
        # display the disease cubes for each city
        if sum(city.disease_cubes.values()) > 0:
            color_location = [location[0], location[1] - stride]
            for cube_color, num_cubes in city.disease_cubes.items():
                if num_cubes > 0:
                    color_location[0] -= stride
                    cube_location = color_location
                    for i in range(num_cubes):
                        pg.draw.circle(screen, colors["white"], [cube_location[0], cube_location[1] - (stride/2) * i], 7)
                        pg.draw.circle(screen, colors[cube_color], [cube_location[0], cube_location[1] - (stride/2) * i], 5)



    # display the location of the players
    locations = {}
    for player in board.players:
        if player.location.name not in locations:
            locations[player.location.name] = [player]
        else:
            locations[player.location.name].append(player)

    for city, players in locations.items():
        city_position = board.cities[city].position
        player_position = [city_position[0] * background.get_width(), city_position[1] * background.get_height()]
        player_position = [player_position[0] + 5 + (2 * radius) / 3, player_position[1] - 10 - (2 * radius) / 3]
        for i in range(len(players)):
            if i % 2 == 0:
                player_position = [player_position[0] + 10, player_position[1] + 10]
            else:
                player_position = [player_position[0], player_position[1] - 10]
            pg.draw.circle(screen, colors[players[i].pawn_color], player_position, 5)


    pg.display.update()


print("Game Over")