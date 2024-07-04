from .city import City
from .color import Color
from .card import (Card, PlayerCard, InfectionCard, EpidemicCard, EventCard,
                   CityCard, Airlift, Forecast, GovernmentGrant, OneQuietNight, ResilientPopulation)
from .player import (Player,
                     ContingencyPlanner, Dispatcher, Medic, OperationsExpert, QuarantineSpecialist, Researcher,
                     Scientist)
from .logger import Logger
from constants import (colors, vertical_card_size,
                       horizontal_card_size, board_size,
                       get_image, radius)

import numpy as np
import pygame as pg

import random
import json
from typing import List, Tuple, Union, Dict
from collections import deque
from math import sin, cos

with open('./configs/pygame.json', 'r') as f:
    pg_settings = json.load(f)

logger = Logger('pandemic-rl-board')

class PandemicBoard:
    def __init__(self, num_epidemics=5, num_players=3, starting_city="Atlanta", seed=None):
        """Initialize the board for Pandemic.
        Contains all the steps of setup in the Pandemic Rules"""

        if seed is not None:
            random.seed(seed)

        self._team_score = 0  # The score to evaluate the Reinforcement Learning model
        # TODO: Implement the score system

        self._resolution = (pg_settings["resolution"][0], pg_settings["resolution"][1])
        self._background_resolution = (int(board_size * self._resolution[0]),
                                       int(board_size * self._resolution[1]))

        if pg_settings["display"] == "windowed":
            self._canvas = pg.display.set_mode(self._resolution, pg.RESIZABLE)
        elif pg_settings["display"] == "fullscreen":
            self._canvas = pg.display.set_mode(self._resolution, pg.FULLSCREEN)
        else:
            raise Warning("Invalid display mode. Must be 'windowed' or 'fullscreen'.")

        pg.init()
        pg.display.set_caption(pg_settings["title"] + " - " + pg_settings["version"])

        self._loc = (1 - board_size) / 2
        self._background_top = int(self._loc * self._resolution[0])
        self._background_left = int(self._loc * self._resolution[1])
        self._last_res = self._resolution

        self._table = get_image('./assets/wood_texture.jpg', self._resolution)
        self._background = get_image('./assets/pandemic_game_board.jpg', self._background_resolution)

        self._colors = {"yellow": Color("yellow"), "red": Color("red"), "blue": Color("blue"), "black": Color("black")}
        self._cities: Dict[str, City] = {}
        self.create_cities(starting_city=starting_city)

        self._connections: List[Tuple[str, str]] = []  # connections between cities

        for city_name, city in self.cities.items():
            for neighbor in self.cities[city_name].neighbors:
                order = tuple(sorted((city.name, neighbor.name)))
                if order not in self._connections:
                    self.connections.append(order)

        if num_epidemics in [4, 5, 6, 7]:
            self.total_epidemics = num_epidemics
        else:
            raise ValueError("Invalid number of epidemics. Must be 4, 5, 6, or 7.")
        self._infection_rate = [2, 2, 2, 3, 3, 4, 4, 4]

        self._outbreaks_curr = 0
        self._outbreaks_max = 8

        self._epidemics_drawn = 0
        self._epidemics_total = num_epidemics

        self._players: List[Player] = []
        self._current_player = 0  # index of the current player in the players list
        self.create_players(num_players, starting_city, role=True)

        self._player_deck: Deque[Card] = []  # converted to a deque during create_player_deck()
        self._player_discard = []
        self.create_player_deck()

        self._infection_deck: Deque[Card] = []  # converted to a deque during create_player_deck()
        self._infection_discard = []
        self.create_infection_deck()

        # Tracks card mechanics
        self.quiet_night = False

    # ------------------------------------------------PROPERTIES--------------------------------------------------------
    @property
    def cities(self) -> Dict[str, City]:
        """Return the cities for the game."""
        return self._cities

    @cities.setter
    def cities(self, cities: dict) -> None:
        """Set the cities for the game."""
        self._cities = cities

    @property
    def connections(self) -> list[Tuple[str, str]]:
        """Return the game board for the game."""
        return self._connections

    @property
    def current_player(self) -> Player:
        """Return the player whose turn it is"""
        return self._players[self._current_player]

    @property
    def epidemics_drawn(self) -> int:
        """Return the number of epidemics drawn."""
        return self._epidemics_drawn

    @epidemics_drawn.setter
    def epidemics_drawn(self, num: int) -> None:
        """Set the number of epidemics drawn."""
        self._epidemics_drawn = num

    @property
    def epidemics_total(self) -> int:
        """Return the total number of epidemics."""
        return self._epidemics_total

    @property
    def infection_discard(self) -> list[InfectionCard]:
        """Return the infection discard pile for the game."""
        return self._infection_discard

    @infection_discard.setter
    def infection_discard(self, discard: list) -> None:
        """Set the infection discard pile for the game."""
        self._infection_discard = discard

    @property
    def player_discard(self) -> list[PlayerCard]:
        """Return the player discard pile for the game."""
        return self._player_discard

    @player_discard.setter
    def player_discard(self, discard: list) -> None:
        """Set the player discard pile for the game."""
        self._player_discard = discard

    @property
    def team_score(self) -> int:
        """Return the team score for the game."""
        return self._team_score

    @property
    def num_outbreaks(self) -> int:
        """Return the number of outbreaks in the game."""
        return self._outbreaks_curr

    @property
    def total_epidemics(self) -> int:
        """Return the total number of epidemics."""
        return self._total_epidemics

    @total_epidemics.setter
    def total_epidemics(self, num: int) -> None:
        """Set the total number of epidemics."""
        self._total_epidemics = num

    @property
    def infection_rate(self) -> int:
        """Return the infection rate for the game."""
        return self._infection_rate[self._epidemics_drawn]

    @property
    def players(self) -> list[Player]:
        """Return the players for the game."""
        return self._players

    @players.setter
    def players(self, players: list) -> None:
        """Set the players for the game."""
        self._players = players

    @property
    def state(self) -> list[int]:  # TODO: Finish this method
        """Return the state of the game as a list of integers"""
        state = []

        city_list = self.city_list()

        for city in city_list:
            state.append(sum(city.disease_cubes.values()))  # The number of disease cubes on each city
            if city.has_research_station:
                state.append(1)
            else:
                state.append(0)
        for player in self.players:
            state.append(city_list.index(player.location))  # The player's position
            # (as the index of the city in the list of cities)
        if len(self.players) < 4:
            for _ in range(len(self.players), 4):
                state.append(0)  # ensure dimensionality stability
        for disease in self._colors.values():  # add the cure/eradication information for each color
            if disease.eradicated:
                state.append(2)
            elif disease.cured:
                state.append(1)
            else:
                state.append(0)

            state.append(color.disease_cubes)  # and the number of cubes left

        state.append(self.infection_rate)

        state.append(self._outbreaks_curr)

        state.append(len(self._player_deck) // 2)  # number of turns remaining

        state.append(self.epidemics_drawn)
        state.append(self.epidemics_total)

        print(f"Warning: Score system is not yet completed")
        return state

    @property
    def turns_remaining(self) -> int:
        """Return the number of turns remaining in the game."""
        return len(self._player_deck) // 2

    # -------------------------------------------------METHODS----------------------------------------------------------
    # Create the game components
    def create_cities(self, starting_city: str = "Atlanta") -> None:
        """Create the cities for the game."""
        logger.print(f"Creating cities. {starting_city} is the starting city.")
        with open("configs/cities.json", "r", encoding='utf-8') as file:
            cities = json.load(file)
        for city in cities:
            self.cities[city["name"]] = City(city["name"], self._colors[city["color"]], city["population"])
            self.cities[city["name"]].position = city["position"]

        for city in cities:
            for neighbor in city["neighbors"]:
                self.cities[city["name"]].add_neighbor(self.cities[neighbor])

        # add research station to starting city
        self.cities[starting_city].has_research_station = True

        logger.print(f"All cities have been created.")

    def create_players(self, num_players: int, starting_city="Atlanta", role=True) -> None:
        """Create the players for the game."""
        logger.print(f"Creating {num_players} players")
        if role:
            roles = [ContingencyPlanner(self, starting_city), Dispatcher(self, starting_city),
                     Medic(self, starting_city), OperationsExpert(self, starting_city),
                     QuarantineSpecialist(self, starting_city), Researcher(self, starting_city),
                     Scientist(self, starting_city)]
            random.shuffle(roles)
            self._players = roles[:num_players]
        else:
            self._players = [Player(self, starting_city=starting_city) for i in range(num_players)]
        logger.print(f"All players have been created.")

    def create_infection_deck(self) -> None:
        """Create the infection deck for the game."""
        logger.print(f"Creating infection deck")
        for city_name, city in self.cities.items():
            self._infection_deck.append(InfectionCard(self, city))
        random.shuffle(self._infection_deck)
        self._infection_deck = deque(self._infection_deck)

        # infect the first 9 cities
        for i in range(1, 4):
            for _ in range(3):
                self.infect_city(num_cubes=i)

        logger.print(f"Infection deck has been created.")

    def create_player_deck(self) -> None:
        """Create the player deck for the game."""
        logger.print(f"Creating the player deck...")
        # Create all the city and event cards
        for city_name, city in self.cities.items():
            self._player_deck.append(CityCard(self, city))
        event_cards = [Airlift(self), Forecast(self), GovernmentGrant(self), OneQuietNight(self),
                       ResilientPopulation(self)]
        for card in event_cards:
            self._player_deck.append(card)

        # deal the players cards
        random.shuffle(self._player_deck)
        num_cards = 6 - len(self._players)
        logger.print(f"\tGiving cards to each player...")
        for player in self._players:
            for _ in range(num_cards):
                card = self._player_deck.pop()
                player.add_to_hand(card)

        # determine player order (highest population city goes first)
        random.shuffle(self._players) # for some reason some event cards tripped up sorting by highest city population
        logger.print(f"It is {self.current_player.role}'s turn")

        # add the epidemic cards
        subdecks = [[EpidemicCard(self)] for _ in range(self.total_epidemics)]
        for i in range(len(self._player_deck)):  # distributing the epidemic cards evenly across the player deck
            subdecks[i % self.total_epidemics].append(self._player_deck[i])

        for deck in subdecks:  # shuffle each subdeck
            random.shuffle(deck)

        self._player_deck = []  # compile each subdeck into the player deck
        for deck in subdecks:
            self._player_deck += deck
        self._player_deck = deque(self._player_deck)
        logger.print(f"The player deck has been created. {self._total_epidemics} epidemics are in the deck.")
    # Game mechanics
    def infect_city(self,
                    num_cubes: int = 1,
                    card: InfectionCard = None) -> None:  # TODO: Test this method for multiple outbreaks at once
        """Infect a city from the top of the infection deck."""

        if not card:
            card = self._infection_deck.pop()
            self._infection_discard.append(card)
        logger.print(f"Infecting {card.city.name} with {num_cubes}")
        color = card.color
        if self._colors[color].disease_cubes < num_cubes:
            self.lose()
            return

        result = card.city.infect(self._colors[color].name, num_cubes)
        if result > 0:  # infect the city (method returns number of outbroken cities)
            self._outbreaks_curr += result
            if self.num_outbreaks >= self._outbreaks_max:
                self.lose()
            return

    def draw_player_cards(self, player: Player = None) -> None:
        """Draw a player card from the top of the player deck."""
        if len(self._player_deck) < 2:
            self.lose()
        if player is None:
            players = self.current_player
        else:
            players = player

        for _ in range(2):
            card = self._player_deck.pop()
            if isinstance(card, EpidemicCard):
                self.epidemic()
                self._player_discard.append(card)
            else:
                logger.print(f"Giving {players.role} card of {card.name}")

                players.add_to_hand(card)

    def draw_infection_cards(self) -> None:
        """Draw the infections for the game."""
        logger.print(f"Drawing infection cards")
        for _ in range(self.infection_rate):
            self.infect_city()

    def epidemic(self) -> None:
        """Handle an epidemic in the game."""
        logger.print("An epidemic was drawn.")
        # Increase
        self._epidemics_drawn += 1

        # Infect
        bottom_card = self._infection_deck.popleft()
        print(f"city {bottom_card.city} has {sum(bottom_card.city._disease_cubes.values())} disease cubes")
        print("Placing 3 disease cubes...")
        self.infect_city(card=bottom_card, num_cubes=3)
        print("Disease cubes placed.")
        self._infection_deck.append(bottom_card)

        if any([any([isinstance(card, ResilientPopulation) for card in player.hand]) for player in self._players]):
            raise NotImplementedError("Put option in for someone to play ResilientPopulation.")

        # Intensify
        random.shuffle(self._infection_discard)
        for card in self._infection_discard:
            self._infection_deck.append(card)
        self._infection_discard = []

    def lose(self):
        """Lose the game."""
        logger.warn("Losing the game has not been implemented yet.")
        self._team_score -= 1000
        raise NotImplementedError("Losing the game is not yet implemented.")


    def next_player(self):
        logger.print(f"Moving to next player")
        self.draw_player_cards()
        self.draw_infection_cards()
        self._current_player = (self._current_player + 1) % len(self._players)

    # ---------------------------------------------DISPLAY METHODS------------------------------------------------------
    def render(self):
        # TODO: Click to view cards in discards
        self.display_background()
        self.display_cities()
        self.display_players()
        self.display_misc()

        pg.display.update()

    def display_background(self):
        self._resolution = self._canvas.get_size()
        if self._resolution != self._last_res:
            self._background_resolution = (int(board_size * self._resolution[0]), int(board_size * self._resolution[1]))
            print(f"Resolution: {self._resolution}")
            print(f"Background resolution: {self._background_resolution}")
            self._background = get_image('assets/pandemic_game_board.jpg', self._background_resolution)
            self._background_top = int(self._loc * self._resolution[0])
            self._background_left = int(self._loc * self._resolution[1])
            self._table = get_image('assets/wood_texture.jpg', self._resolution)
            self._last_res = self._resolution
        self._canvas.blit(self._table, (0, 0))
        self._canvas.blit(self._background, (self._background_top, self._background_left))

    def display_cities(self):
        city_radius = radius * board_size * (self._canvas.get_width() / 2560)
        self.display_connections()
        for city_name, city in self.cities.items():
            # horizontal, vertical
            # left-right, top-down
            location = self.on_background([city.position[0], city.position[1]])

            # display a white outline if the city has a research station
            if city.has_research_station:
                pg.draw.circle(self._canvas, colors["white"],
                               (location[0], location[1]),
                               int(city_radius * 1.1) + 1)

            # display the city as a circle
            pg.draw.circle(self._canvas,
                           colors[city.color.name],
                           (location[0], location[1]),
                           city_radius)

            stride = city_radius
            cube_size = city_radius / 2
            # display the disease cubes for each city
            if sum(city.disease_cubes.values()) > 0:
                color_location = [location[0], location[1] - stride]
                for cube_color, num_cubes in city.disease_cubes.items():
                    if num_cubes > 0:
                        color_location[0] -= stride
                        cube_location = color_location
                        for i in range(num_cubes):
                            pg.draw.circle(self._canvas,  # white border
                                           colors["white"],
                                           [cube_location[0], cube_location[1] - (stride / 2) * i],
                                           1.25 * cube_size)
                            pg.draw.circle(self._canvas,  # cube color fill
                                           colors[cube_color],
                                           [cube_location[0], cube_location[1] - (stride / 2) * i],
                                           cube_size)

    def display_connections(self):
        border = (1 - board_size) / 2
        exception1 = ['San Francisco', 'Los Angeles']
        exception2 = ['Sydney', 'Manila', 'Tokyo']  # cities on the edge of the board
        for connection in self.connections:
            location_1 = self.on_background([self.cities[connection[0]].position[0],
                                             self.cities[connection[0]].position[1]])
            location_2 = self.on_background([self.cities[connection[1]].position[0],
                                             self.cities[connection[1]].position[1]])
            if (connection[0] in exception1 and connection[1] in exception2 or
                    connection[0] in exception2 and connection[1] in exception1):

                midpoint_y = np.mean([location_1[1], location_2[1]])
                locations = sorted([location_1, location_2], key=lambda x: x[0])
                pg.draw.line(self._canvas, colors["white"], locations[0],
                             (border * self._canvas.get_width(), midpoint_y))
                pg.draw.line(self._canvas, colors["white"], locations[1],
                             ((1 - border) * self._canvas.get_width(), midpoint_y))
            else:
                pg.draw.line(self._canvas, colors["white"], location_1, location_2)

    def display_player_hands(self):
        # raise NotImplementedError("Finish Implementing Drawing of Player Hands dipwad")
        border = (1 - board_size) / 2
        board_coords = {
            "top left": [border, border],
            "top right": [(1 - border), border],
            "bottom left": [border, (1 - border)],
            "bottom right": [(1 - border), (1 - border)]
        }

        locs = {
            "left": [0.1 * board_coords["top left"][0],
                     board_coords["top left"][1],
                     border * 0.8,
                     board_size],
            "bottom": [board_coords["bottom left"][0],
                       board_coords["bottom left"][1] + (0.1 * border),
                       board_size,
                       border * 0.8],
            "right": [board_coords["top right"][0] + (0.1 * border),
                      board_coords["top right"][1],
                      border * 0.8,
                      board_size],
            "top": [board_coords["top left"][0],  # x coord of top left
                    board_coords["top left"][1] * 0.1,  # y coord of top left
                    board_size,  # width
                    border * 0.8]  # height
        }

        rects = {}
        for key, value in locs.items():
            temp = self.on_table(value)
            rects[key] = pg.Rect(temp[0], temp[1], temp[2], temp[3])

        horizontal_offset = 0.1 * (board_size / 0.75)
        vertical_offset = 0.125 * (board_size / 0.75)

        if len(self.players) == 2:
            starting_location = locs["top"][:2]
            starting_location[0] += 0.01 * (board_size / 0.65)
            starting_location[1] += 0.005 * (board_size / 0.65)

            pg.draw.rect(self._canvas,
                         colors[self.players[0].pawn_color],
                         rects["top"],
                         0,
                         10)

            for card in self.players[0].hand:
                self.display_card(card, starting_location, on_background=False)
                starting_location[0] += horizontal_offset

            # add player hand here

            pg.draw.rect(self._canvas,
                         colors[self.players[1].pawn_color],
                         rects["bottom"],
                         0,
                         10)

            # add player hand here
            starting_location = locs["bottom"][:2]
            starting_location[0] += 0.01 * (board_size / 0.65)
            starting_location[1] += 0.005 * (board_size / 0.65)

            for card in self.players[1].hand:
                self.display_card(card, starting_location, on_background=False)
                starting_location[0] += horizontal_offset

        else:
            counter = 0
            for key, rect in rects.items():
                if counter == len(self.players):
                    break
                pg.draw.rect(self._canvas,
                             colors[self.players[counter].pawn_color],
                             rect,
                             0,
                             10)

                starting_location = locs[key][:2]
                if key == 'right' or key == 'left':
                    starting_location[0] += 0.025 * (board_size / 0.65)
                    starting_location[1] += 0.01 * (board_size / 0.65)
                    for card in self.players[counter].hand:
                        self.display_card(card, starting_location, sideways=True, on_background=False)
                        starting_location[1] += vertical_offset
                else:
                    starting_location[0] += 0.01 * (board_size / 0.65)
                    starting_location[1] += 0.005 * (board_size / 0.65)
                    for card in self.players[counter].hand:
                        self.display_card(card, starting_location, on_background=False)
                        starting_location[0] += horizontal_offset

                counter += 1

    def display_players(self):
        player_radius = radius * (self._canvas.get_width() / 2560)
        locations = {}  # store the players locations
        for player in self.players:
            if player.location.name not in locations:
                locations[player.location.name] = [player]
            else:
                locations[player.location.name].append(player)

        for city, players in locations.items():
            city_position = self.on_background(self.cities[city].position)
            player_position = [city_position[0] + (player_radius) / 3, city_position[1] - player_radius]
            for i in range(len(players)):
                interval = player_radius
                if i % 2 == 0:  # make sure that the players appear as a square
                    player_position = [player_position[0] + interval, player_position[1] + interval]
                else:
                    player_position = [player_position[0], player_position[1] - interval]
                pg.draw.circle(self._canvas,
                               colors[players[i].pawn_color],
                               player_position,
                               player_radius // 2)

        self.display_player_hands()

    def display_misc(self):
        self.display_trackers()
        self.display_decks()

    def display_card(self,
                     card: Card,
                     location: Union[List[float], Tuple[float, float]],
                     sideways: bool = False,
                     face_up: bool = True,
                     on_background: bool = True) -> None:
        """
        Displays a single PlayerCard on the screen at a specified location

        :param card: The PlayerCard to display
        :param location: The location, as a pair of floats (0 <= x <= 1 for each value)
        :param sideways: Whether the card is displayed on its side
        :param face_up: Whether the card is up or down
        """

        # Check variables
        if sideways:
            size = horizontal_card_size  # TODO: Update this to look good for displaying cards sideways
        else:
            size = vertical_card_size

        if not on_background:
            size = tuple([board_size * val for val in size])

        if len(location) != 2:
            raise ValueError(f"location must have length 2, not {len(location)}")
        for val in location:
            if not 0 <= val <= 1:
                raise ValueError(f"values in location must be between 0 and 1, actual location: {val}")

        # create some constants
        border = 10 * (self._canvas.get_width() / 2560)  # determine border thickness
        border_radius = int(10 * (self._canvas.get_width() / 2560))
        font = pg.font.SysFont("arial", int(48 * board_size * (self._canvas.get_width() / 2560)))

        # determine the display color of the border
        if isinstance(card, PlayerCard):
            border_color = colors["cyan"]
        elif isinstance(card, InfectionCard):
            border_color = colors["black"]
        else:
            raise TypeError(f"Unrecognized card type: {type(card)}")

        # determine the display color of the card
        if face_up:
            if isinstance(card, PlayerCard):
                card_color = colors[card.color]
            else:
                card_color = colors[card.city.color.name]
        else:
            if isinstance(card, InfectionCard):
                card_color = colors["dark green"]
            else:
                card_color = colors["blue"]

        # determine the text to be displayed on card
        if face_up:
            card_text = card.name
        else:
            if isinstance(card, InfectionCard):
                card_text = str(len(self._infection_deck))
            else:
                card_text = str(len(self._player_deck))
        if on_background:
            center = self.on_background([location[0] + size[0] / 2, location[1] + size[1] / 2])
        else:
            center = self.on_table([location[0] + size[0] / 2, location[1] + size[1] / 2])

        loc = location + list(size)

        if on_background:
            loc = self.on_background(loc)
        else:
            loc = self.on_table(loc)

        # card outline
        pg.draw.rect(self._canvas,
                     border_color,
                     pg.Rect(loc[0],
                             loc[1],
                             loc[2],
                             loc[3]),
                     0,
                     border_radius)

        # backing matches card color
        pg.draw.rect(self._canvas,
                     card_color,
                     pg.Rect(loc[0] + border,
                             loc[1] + border,
                             loc[2] - 2 * border,
                             loc[3] - 2 * border),
                     0,
                     border_radius)

        # display the card name on the card
        text_color = tuple([255 - val for val in card_color])
        text = font.render(card_text, True, text_color)
        textRect = text.get_rect()
        textRect.center = center
        self._canvas.blit(text, textRect)

    def display_trackers(self):
        font = pg.font.SysFont("arial", int(48 * board_size * (self._canvas.get_width() / 2560)))
        # Draw the infection rate tracker
        tracker_radius = radius * board_size * (self._canvas.get_width() / 2560) * 1.1
        coeff = self._epidemics_drawn
        location = self.on_background([0.643 + coeff * 0.034, 0.233])
        pg.draw.circle(self._canvas,
                       colors["dark green"],
                       location,
                       tracker_radius)

        # Draw cure trackers
        location = [0.34, 0.9325]
        cure_distance = 0.065
        color_space = 0.046
        for name, color in self._colors.items():
            if color.cured:
                location[1] -= cure_distance
            loc = self.on_background(location)
            pg.draw.circle(self._canvas, colors[name], loc, tracker_radius)
            if name == 'yellow':
                display_color = colors['black']
            else:
                display_color = colors['white']

            if color.eradicated:
                val = 'E'
            else:
                val = str(color.disease_cubes)

            text = font.render(val, True, display_color)
            textRect = text.get_rect()
            textRect.center = loc
            self._canvas.blit(text, textRect)
            location[0] += color_space
            if color.cured:
                location[1] += cure_distance
            if name == 'blue':
                location[0] -= 0.0035

        # Draw outbreak tracker
        coeff = self._outbreaks_curr
        location = [0.079, 0.56125]
        v_dist = 0.0405
        h_dist = 0.035

        if coeff % 2 == 1:
            location[0] += h_dist
        location[1] += v_dist * coeff
        loc = self.on_background(location)
        pg.draw.circle(self._canvas, colors["dark green"], loc, tracker_radius)

        # TODO: Draw cube total trackers

    def display_decks(self):
        deck_location = [0.5975, 0.058]
        offset = 0.1625  # determine distance between draw & discard piles on board
        font = pg.font.SysFont("arial", int(48 * board_size * (self._canvas.get_width() / 2560)))

        # Draw the infection deck
        self.display_card(self._infection_deck[-1],
                          deck_location,
                          sideways=True,
                          face_up=False)

        # Draw infection discard
        if len(self._infection_discard) > 0:
            deck_location[0] += offset
            self.display_card(self.infection_discard[-1],
                              deck_location,
                              sideways=True)

            # number of cards in discard
            text = font.render(str(len(self.infection_discard)), True, colors["dark green"])
            textRect = text.get_rect()
            textRect.center = self.on_background([deck_location[0] + (horizontal_card_size[0] / 2),
                                                  deck_location[1] + (horizontal_card_size[1] / 2) - 0.045])
            self._canvas.blit(text, textRect)

        # Draw player deck
        deck_location = [0.6, 0.735]
        offset = 0.1325

        self.display_card(self._player_deck[-1],
                          deck_location,
                          face_up=False)

        # Draw player discard
        if len(self.player_discard) > 0:
            deck_location[0] += offset
            self.display_card(self.player_discard[-1],
                              deck_location)

            # Write name of city on top of discard
            text = font.render(str(len(self.player_discard)), True, colors["white"])
            textRect = text.get_rect()
            textRect.center = self.on_background([deck_location[0] + (vertical_card_size[0] / 2),
                                                  deck_location[1] + (vertical_card_size[1] / 2) - 0.045])
            self._canvas.blit(text, textRect)

    # TODO: make locations of trackers variables
    # (cut down on calculations on a per-frame basis)

    # ----------------------------------------- HELPER METHODS --------------------------------------------------------
    def city_list(self) -> List[City]:
        """All the cities in the board in sorted order by name"""
        return sorted(list(self.cities.values()))

    def emergency_path(self, start_city_name: str) -> list:
        """Find the shortest path between start_city and a city with 3 cubes on it using BFS."""
        if start_city_name not in self._cities.keys():
            raise ValueError("The specified city does not exist.")

        max_cubes = sum(max(self.cities.values(), key= lambda x: sum(x._disease_cubes.values()))._disease_cubes.values())

        start_city = self._cities[start_city_name]

        # Initialize the queue with the start city and a path containing just the start city
        queue = deque([(start_city, [start_city_name])])
        visited = set()

        while queue:
            current_city, path = queue.popleft()

            if current_city.name in visited:
                continue

            # Mark the current city as visited
            visited.add(current_city.name)

            # Check if we have reached the end city
            if sum(current_city._disease_cubes.values()) >= max_cubes:
                return path

            # Add neighbors to the queue
            for neighbor in current_city.neighbors:
                if neighbor.name not in visited:
                    queue.append((neighbor, path + [neighbor.name]))

        # Return an empty list if there is no path
        return []

    def shortest_path(self, start_city_name: str, end_city_name: str) -> list:
        """Find the shortest path between two cities using BFS."""
        if start_city_name not in self._cities.keys() or end_city_name not in self._cities.keys():
            raise ValueError("One or both of the specified cities do not exist.")

        start_city = self._cities[start_city_name]
        end_city = self._cities[end_city_name]

        # Initialize the queue with the start city and a path containing just the start city
        queue = deque([(start_city, [start_city_name])])
        visited = set()

        while queue:
            current_city, path = queue.popleft()

            if current_city.name in visited:
                continue

            # Mark the current city as visited
            visited.add(current_city.name)

            # Check if we have reached the end city
            if current_city.name == end_city_name:
                return path

            # Add neighbors to the queue
            for neighbor in current_city.neighbors:
                if neighbor.name not in visited:
                    queue.append((neighbor, path + [neighbor.name]))

        # Return an empty list if there is no path
        return []

        # TODO: Add rendering of player hands

    def on_background(self, location: List[float]) -> List[int]:
        """Convert a relative position to an absolute position on the board background.
        (a pair of nums representing what % of the board it is to pixel nums)

        param location: the pair of nums representing what % of the board something is located at"""

        border = (1 - board_size) / 2
        if len(location) % 2 != 0:
            raise ValueError("location must be a an even number of floats")
        for val in location:
            if val < 0 or val > 1:
                raise ValueError(f"Location values must be between 0 and 1, not {val}")

        loc = [board_size * coord for coord in location]  # scale it to the size of the board
        loc[0] += border  # to compensate for the board being centered
        loc[1] += border

        for i in range(len(location)):  # get the pixel numbers
            if i % 2 == 0:
                loc[i] *= self._canvas.get_width()
            else:
                loc[i] *= self._canvas.get_height()

            loc[i] = int(loc[i])

        return loc

    def on_table(self, location: List[float]) -> List[int]:
        """Convert a relative position to an absolute position that is NOT on the board, but instead on the table"""
        border = (1 - board_size) / 2
        if len(location) % 2 != 0:
            raise ValueError("location must be a an even number of floats")
        for val in location:
            if val < 0 or val > 1:
                raise ValueError(f"Location values must be between 0 and 1, given {val}")
        if border < location[0] < 1 - border and border < location[1] < 1 - border:
            raise ValueError(f"Location values must be on the border of the table,\n"
                             f"between {border} and {1 - border}, given {location[0]} and {location[1]}")
            # print("card failed to display, locations not correct")

        loc = [val for val in location] # to prevent any funny business with memory sharing

        for i in range(len(location)):  # get the pixel numbers
            if i % 2 == 0:
                loc[i] *= self._canvas.get_width()
            else:
                loc[i] *= self._canvas.get_height()

            loc[i] = int(loc[i])

        return loc