import pygame as pg
import json
from utils.board import PandemicBoard


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
background = pg.image.load("assets/pandemic_game_board.jpg")
background_top = 0
background_left = 0
# initialize the Pandemic board
board = PandemicBoard()

board.player_discard.append(board._player_deck.pop())
board.player_discard.append(board._player_deck.pop())

running = True


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

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # display the background
    screen.blit(background, (background_top, background_left))

    # TODO: cure tracker

    # TODO: outbreak tracker

    # TODO: Turn remaining counter

    # TODO: Player Card Deck/tracker

    # TODO: Click to view cards in discards


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
            interval = 20
            if i % 2 == 0:
                player_position = [player_position[0] + interval, player_position[1] + interval]
            else:
                player_position = [player_position[0], player_position[1] - interval]
            pg.draw.circle(screen, colors[players[i].pawn_color], player_position, 10)

    # Draw the outbreak tracker
    location = [0.643, 0.233]
    coeff = board._outbreaks_curr
    location = [int((location[0] + coeff * 0.034) * background.get_width()), int(location[1] * background.get_height())]
    pg.draw.circle(screen, colors["dark green"], location, 25)



    # draw infection deck
    # location = [left, top, width, height]
    coeffs = [0.5975, 0.058, 0.14, 0.14]

    font = pg.font.SysFont("arial", 48)
    text = font.render(str(len(board._infection_deck)), True, colors["white"])
    textRect = text.get_rect()
    textRect.center = [int((coeffs[0] + (coeffs[2] / 2)) * background.get_width()),
                       int((coeffs[1] + (coeffs[3] / 2)) * background.get_height())]

    location = [int(coeffs[i] * background.get_width()) if i % 2 == 0 else int(coeffs[i] * background.get_height()) for i in range(len(coeffs))]
    pg.draw.rect(screen,
                 colors["black"],
                 pg.Rect(location[0],
                         location[1],
                         location[2],
                         location[3]),
                 0,
                 10) # black card outline
    pg.draw.rect(screen,
                 colors["dark green"],
                 pg.Rect(location[0] + 10,
                         location[1] + 10,
                         location[2] - 20,
                         location[3] - 20),
                 0,
                 10) # green backing
    screen.blit(text, textRect) # number of cards left in discard

    # draw infection discard
    if len(board._infection_discard) > 0:
        text = font.render(board._infection_discard[-1]._city.name, True, colors["dark green"])
        textRect = text.get_rect()
        textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.16) * background.get_width()),
                           int((coeffs[1] + (coeffs[3] / 2)) * background.get_height())]

        location = [int(coeffs[i] * background.get_width()) if i % 2 == 0 else int(coeffs[i] * background.get_height()) for
                    i in range(len(coeffs))]
        pg.draw.rect(screen,
                     colors["white"],
                     pg.Rect(location[0] + (0.13 * screen.get_width()),
                             location[1],
                             location[2],
                             location[3]),
                     0,
                     10)  # white card outline
        pg.draw.rect(screen,
                     colors[board.infection_discard[-1]._color.name],
                     pg.Rect(location[0] + 10 + (0.13 * screen.get_width()),
                             location[1] + 10,
                             location[2] - 20,
                             location[3] - 20),
                     0,
                     10)  # backing matches city color
        screen.blit(text, textRect)  # name of last drawn infection card

        text = font.render(str(len(board._infection_discard)), True, colors["dark green"])
        textRect = text.get_rect()
        textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.11) * background.get_width()),
                           int((coeffs[1] + (coeffs[3] / 2) - 0.045) * background.get_height())]

        screen.blit(text, textRect)

    # Draw player deck
    # location = [left, top, width, height]
    coeffs = [0.6, 0.735, 0.1, 0.2]

    text = font.render(str(len(board._player_deck)), True, colors["white"])
    textRect = text.get_rect()
    textRect.center = [int((coeffs[0] + (coeffs[2] / 2)) * background.get_width()),
                       int((coeffs[1] + (coeffs[3] / 2)) * background.get_height())]
    location = [int(coeffs[i] * background.get_width()) if i % 2 == 0 else int(coeffs[i] * background.get_height()) for i in range(len(coeffs))]
    pg.draw.rect(screen, colors["cyan"], pg.Rect(location[0], location[1], location[2], location[3]), 0, 10) # cyan card outline
    pg.draw.rect(screen, colors["blue"], pg.Rect(location[0] + 10, location[1] + 10, location[2] - 20, location[3] - 20), 0, 10) # blue backing
    screen.blit(text, textRect) # name of city on top of discard

    # Draw player discard
    if len(board.player_discard) > 0:
        text = font.render(board.player_discard[-1].name, True, tuple([255 - val for val in colors[board.player_discard[-1].display_color]]))
        textRect = text.get_rect()
        textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.13) * background.get_width()),
                           int((coeffs[1] + (coeffs[3] / 2)) * background.get_height())]

        location = [int(coeffs[i] * background.get_width()) if i % 2 == 0 else int(coeffs[i] * background.get_height())
                    for
                    i in range(len(coeffs))]
        pg.draw.rect(screen,
                     colors["white"],
                     pg.Rect(location[0] + (0.1055 * screen.get_width()),
                             location[1],
                             location[2],
                             location[3]),
                     0,
                     10)  # white card outline
        pg.draw.rect(screen,
                     colors[board.player_discard[-1].display_color],
                     pg.Rect(location[0] + 10 + (0.1055 * screen.get_width()),
                             location[1] + 10,
                             location[2] - 20,
                             location[3] - 20),
                     0,
                     10)  # backing matches city color
        screen.blit(text, textRect)  # name of card on top of discard

        text = font.render(str(len(board._player_discard)), True, colors["cyan"])
        textRect = text.get_rect()
        textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.1) * background.get_width()),
                           int((coeffs[1] + (coeffs[3] / 2) - 0.07) * background.get_height())]

        screen.blit(text, textRect)

    pg.display.update()

print("Game Over")