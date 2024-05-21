from .city import City
from .color import Color
from .player_card import PlayerCard, CityCard, EpidemicCard, EventCard, Airlift, Forecast, GovernmentGrant, OneQuietNight, ResilientPopulation
from .player import Player, ContingencyPlanner, Dispatcher, Medic, OperationsExpert, QuarantineSpecialist, Researcher, Scientist
from .infection_card import InfectionCard
from constants import colors

import numpy as np
import pygame as pg

import random
import json
from typing import List
from collections import deque

pg_settings = json.load(open("configs/pygame.json", "r"))
radius = pg_settings["city_circle_radius"]
class PandemicBoard:
    def __init__(self, canvas, num_epidemics=5, num_players=3, starting_city="Atlanta"):
        """Initialize the board for Pandemic.
        Contains all the steps of setup in the Pandemic Rules"""

        self._team_score = 0 # The score to evaluate the Reinforcement Learning model
        # TODO: Implement the score system

        self._canvas = canvas

        # STEP 0: Create the basic game components
        self._colors = {"blue": Color("blue"), "yellow": Color("yellow"), "black": Color("black"), "red": Color("red")}
        self._cities = {}
        self.create_cities(starting_city=starting_city)

        self._connections = [] # connections between cities

        for city_name, city in self.cities.items():
            for neighbor in self.cities[city_name].neighbors:
                order = tuple(sorted((city.name, neighbor.name)))
                if order not in self.connections:
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

        self._players = []
        self._current_player = 0 # index of the current player in the players list
        self.create_players(num_players, starting_city, role=True)

        self._player_deck = []
        self._player_discard = []
        self.create_player_deck()

        self._infection_deck = []
        self._infection_discard = []
        self.create_infection_deck()

        # Tracks card mechanics
        self.quiet_night = False

    # ------------------------------------------------PROPERTIES--------------------------------------------------------
    @property
    def cities(self) -> dict:
        """Return the cities for the game."""
        return self._cities

    @cities.setter
    def cities(self, cities: dict) -> None:
        """Set the cities for the game."""
        self._cities = cities

    @property
    def connections(self) -> list[City]:
        """Return the game board for the game."""
        return self._connections

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

    @num_outbreaks.setter
    def num_outbreaks(self, num: int) -> None:
        """Set the number of outbreaks in the game."""
        self._num_outbreaks = num

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
    def state(self) -> list[int]: # TODO: Finish this method
        """Return the state of the game as a list of integers"""
        state = []

        city_list = self.city_list()

        for city in city_list:
            state.append(sum(city.disease_cubes.values())) # The number of disease cubes on each city
            if city.has_research_station:
                state.append(1)
            else:
                state.append(0)
        for player in self.players:
            state.append(city_list.index(player.location)) # The player's position
                                                           # (as the index of the city in the list of cities)
        if len(self.players) < 4:
            for _ in range(len(self.players), 4):
                state.append(0) # ensure dimensionality stability
        for disease in self._colors.values(): # add the cure/eradication information for each color
            if disease.eradicated:
                state.append(2)
            elif disease.cured:
                state.append(1)
            else:
                state.append(0)

            state.append(color.disease_cubes) # and the number of cubes left

        state.append(self.infection_rate)

        state.append(self._outbreaks_curr)

        state.append(len(self._player_deck) // 2) # number of turns remaining

        state.append(self.epidemics_drawn)
        state.append(self.epidemics_total)

        print(f"Warning: Score system is not yet completed")
        return state

    def turns_remaining(self) -> int:
        """Return the number of turns remaining in the game."""
        return len(self._player_deck) // 2

    # -------------------------------------------------METHODS----------------------------------------------------------

    # Create the game components
    def create_cities(self, starting_city: str="Atlanta") -> None:
        """Create the cities for the game."""
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

    def create_players(self, num_players: int, starting_city="Atlanta", role=True) -> None:
        """Create the players for the game."""

        if role:
            roles = [ContingencyPlanner(self,starting_city), Dispatcher(self, starting_city),
                    Medic(self, starting_city), OperationsExpert(self, starting_city),
                    QuarantineSpecialist(self, starting_city), Researcher(self, starting_city),
                    Scientist(self, starting_city)]
            random.shuffle(roles)
            self._players = roles[:num_players]
        else:
            self._players = [Player(self, starting_city=starting_city) for i in range(num_players)]

    def create_infection_deck(self) -> None:
        """Create the infection deck for the game."""
        # create the infection deck
        for city_name, city in self.cities.items():
            self._infection_deck.append(InfectionCard(city))
        random.shuffle(self._infection_deck)

        # infect the first 9 cities
        for i in range(1, 4):
            for _ in range(3):
                card = self._infection_deck.pop()
                city = card.city
                color = city.color

                city.infect(color.name, num_cubes=i)

                self._infection_discard.append(card)

    def create_player_deck(self) -> None:
        """Create the player deck for the game."""
        # Create all the city and event cards
        for city_name, city in self.cities.items():
            self._player_deck.append(CityCard(self, city))
        event_cards = [Airlift(self), Forecast(self), GovernmentGrant(self), OneQuietNight(self), ResilientPopulation(self)]
        for card in event_cards:
            self._player_deck.append(card)

        # deal the players cards
        random.shuffle(self._player_deck)
        num_cards = 6 - len(self._players)
        for player in self._players:
            for _ in range(num_cards):
                player.add_to_hand(self._player_deck.pop())

        # determine player order (highest population city goes first)
        self._players.sort(key=lambda x: max(x.hand, key=lambda y: isinstance(y, CityCard)).city.population, reverse=True)

        # add the epidemic cards
        subdecks = [[EpidemicCard(self)] for _ in range(self.total_epidemics)]
        for i in range(len(self._player_deck)): # distributing the epidemic cards evenly across the player deck
            subdecks[i % self.total_epidemics].append(self._player_deck[i])

        for deck in subdecks: # shuffle each subdeck
            random.shuffle(deck)

        self._player_deck = [] # compile each subdeck into the player deck
        for deck in subdecks:
            self._player_deck += deck

    # Game mechanics
    def infect_city(self, num_cubes:int=1, card:InfectionCard=None) -> None: # TODO: Test this method for multiple outbreaks at once
        """Infect a city from the top of the infection deck."""
        if self.quiet_night:
            self.quiet_night = False
            return

        if not card:
            card = self._infection_deck.pop()
            self._infection_discard.append(card)
        color = card.color
        if color.disease_cubes < num_cubes:
            self.lose()
            return

        result = card.city.infect(color.name, num_cubes)
        if result > 0: # infect the city (method returns number of outbroken cities)
                self.num_outbreaks += result
                if self.num_outbreaks >= self._outbreaks_max:
                    self.lose()
                return

    def draw_player_card(self, player:Player) -> None:
        """Draw a player card from the top of the player deck."""
        if len(self._player_deck) < 2:
            self.lose()
        for _ in range(2):
            card = self._player_deck.pop()
            if isinstance(card, EpidemicCard):
                self.epidemic()
                self._player_discard.append(card)
            else:
                player.add_to_hand(card)

    def draw_infection_card(self) -> None:
        """Draw the infections for the game."""
        for _ in range(self.infection_rate):
            self.infect_city(1)

    def epidemic(self) -> None:
        """Handle an epidemic in the game."""
        print("Oops, an epidemic!")
        # Increase
        self._epidemics_drawn += 1

        # Infect
        bottom_card = self._infection_deck.pop(0)
        self.infect_city(card=bottom_card, num_cubes=3)
        self._infection_deck.append(bottom_card)

        if any([any([isinstance(card, ResilientPopulation) for card in player.hand]) for player in self._players]):
            raise NotImplementedError("Put option in for someone to play ResilientPopulation.")

        # Intensify
        random.shuffle(self._infection_discard)
        for card in self._infection_discard:
            self._infection_deck.insert(0, card)
        self._infection_discard = []

    def lose(self):
        """Lose the game."""
        raise NotImplementedError("Losing the game is not yet implemented.")

    # ---------------------------------------------DISPLAY METHODS------------------------------------------------------
    def draw(self):
        self.display_cities()
        self.display_players()
        self.display_misc()

    def display_cities(self):
        city_radius = radius * (self._canvas.get_width() / 2560)
        self.display_connections()
        for city_name, city in self.cities.items():
            # horizontal, vertical
            # left-right, top-down
            location = [int(city.position[0] * self._canvas.get_width()),
                        int(city.position[1] * self._canvas.get_height())]

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

            stride = int(city_radius * 1.1)
            # display the disease cubes for each city
            if sum(city.disease_cubes.values()) > 0:
                color_location = [location[0], location[1] - stride]
                for cube_color, num_cubes in city.disease_cubes.items():
                    if num_cubes > 0:
                        color_location[0] -= stride
                        cube_location = color_location
                        for i in range(num_cubes):
                            pg.draw.circle(self._canvas, # white border
                                           colors["white"],
                                           [cube_location[0], cube_location[1] - (stride / 2) * i],
                                           city_radius // 3)
                            pg.draw.circle(self._canvas, # cube color fill
                                           colors[cube_color],
                                           [cube_location[0], cube_location[1] - (stride / 2) * i],
                                           city_radius // 4)

    def display_connections(self):
        exception1 = ['San Francisco', 'Los Angeles']
        exception2 = ['Sydney', 'Manila', 'Tokyo'] # cities on the edge of the board
        for connection in self.connections:
            location_1 = [int(self.cities[connection[0]].position[0] * self._canvas.get_width()),
                          int(self.cities[connection[0]].position[1] * self._canvas.get_height())]
            location_2 = [int(self.cities[connection[1]].position[0] * self._canvas.get_width()),
                          int(self.cities[connection[1]].position[1] * self._canvas.get_height())]
            if connection[0] in exception1 and connection[1] in exception2 or connection[0] in exception2 and connection[1] in exception1:
                midpoint_y = np.mean([location_1[1], location_2[1]])
                locations = sorted([location_1, location_2], key=lambda x: x[0])
                pg.draw.line(self._canvas, colors["white"], locations[0], (0, midpoint_y))
                pg.draw.line(self._canvas, colors["white"], locations[1], (self._canvas.get_width(), midpoint_y))
            else:
                pg.draw.line(self._canvas, colors["white"], location_1, location_2)

    def display_players(self):
        player_radius = radius * (self._canvas.get_width() / 2560)
        locations = {} # store the players locations
        for player in self.players:
            if player.location.name not in locations:
                locations[player.location.name] = [player]
            else:
                locations[player.location.name].append(player)

        for city, players in locations.items():
            city_position = self.cities[city].position
            city_position = [city_position[0] * self._canvas.get_width(), city_position[1] * self._canvas.get_height()]
            player_position = [city_position[0] + (2 * player_radius) / 3, city_position[1] - (2 * player_radius) / 3]
            for i in range(len(players)):
                interval = player_radius
                if i % 2 == 0: # make sure that the players appear as a square
                    player_position = [player_position[0] + interval, player_position[1] + interval]
                else:
                    player_position = [player_position[0], player_position[1] - interval]
                pg.draw.circle(self._canvas,
                               colors[players[i].pawn_color],
                               player_position,
                               player_radius // 2)

    def display_misc(self):
        self.display_trackers()
        self.display_decks()

    def display_trackers(self):
        # Draw the outbreak tracker
        tracker_radius = radius * (self._canvas.get_width() / 2560) * 1.1
        location = [0.643, 0.233]
        coeff = self._epidemics_drawn
        location = [int((location[0] + coeff * 0.034) * self._canvas.get_width()), int(location[1] * self._canvas.get_height())]
        pg.draw.circle(self._canvas,
                       colors["dark green"],
                       location,
                       tracker_radius)

        # TODO: Draw cure trackers
        # TODO: Draw cube total trackers

    def display_decks(self):
        border = 10 * (self._canvas.get_width() / 2560) # determine border thickness
        offset = (0.1625 * self._canvas.get_width()) # determine distance between draw & discard piles on board

        # Draw the infection deck
        # location = [left, top, width, height]
        coeffs = [0.5975, 0.058, 0.14, 0.14] # fit the card to the right place & size on the board
        font = pg.font.SysFont("arial", int(48 * (self._canvas.get_width() / 2560)))
        text = font.render(str(len(self._infection_deck)), True, colors["white"])
        textRect = text.get_rect()
        textRect.center = [int((coeffs[0] + (coeffs[2] / 2)) * self._canvas.get_width()),
                           int((coeffs[1] + (coeffs[3] / 2)) * self._canvas.get_height())]

        location = [int(coeffs[i] * self._canvas.get_width()) if i % 2 == 0 else int(coeffs[i] * self._canvas.get_height())
                    for i in range(len(coeffs))]
        pg.draw.rect(self._canvas,
                     colors["black"],
                     pg.Rect(location[0],
                             location[1],
                             location[2],
                             location[3]),
                     0,
                     10)  # black card outline
        pg.draw.rect(self._canvas,
                     colors["dark green"],
                     pg.Rect(location[0] + border,
                             location[1] + border,
                             location[2] - 2*border,
                             location[3] - 2*border),
                     0,
                     10)  # green backing
        self._canvas.blit(text, textRect)  # number of cards left in discard

        # draw infection discard
        if len(self._infection_discard) > 0:
            text = font.render(self._infection_discard[-1]._city.name, True, colors["dark green"])
            textRect = text.get_rect()
            textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.16) * self._canvas.get_width()),
                               int((coeffs[1] + (coeffs[3] / 2)) * self._canvas.get_height())]

            location = [int(coeffs[i] * self._canvas.get_width()) if i % 2 == 0 else int(coeffs[i] * self._canvas.get_height())
                        for i in range(len(coeffs))]

            pg.draw.rect(self._canvas,
                         colors["white"],
                         pg.Rect(location[0] + offset,
                                 location[1],
                                 location[2],
                                 location[3]),
                         0,
                         10)  # white card outline
            pg.draw.rect(self._canvas,
                         colors[self.infection_discard[-1]._color.name],
                         pg.Rect(location[0] + border + offset,
                                 location[1] + border,
                                 location[2] - 2*border,
                                 location[3] - 2*border),
                         0,
                         10)  # backing matches city color
            self._canvas.blit(text, textRect)  # name of last drawn infection card

            text = font.render(str(len(self._infection_discard)), True, colors["dark green"])
            textRect = text.get_rect()
            textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.11) * self._canvas.get_width()),
                               int((coeffs[1] + (coeffs[3] / 2) - 0.045) * self._canvas.get_height())]

            self._canvas.blit(text, textRect)

        # Draw player deck
        # location = [left, top, width, height]
        coeffs = [0.6, 0.735, 0.1, 0.2]
        offset = (0.1325 * self._canvas.get_width())
        text = font.render(str(len(self._player_deck)), True, colors["white"])
        textRect = text.get_rect()
        textRect.center = [int((coeffs[0] + (coeffs[2] / 2)) * self._canvas.get_width()),
                           int((coeffs[1] + (coeffs[3] / 2)) * self._canvas.get_height())]
        location = [int(coeffs[i] * self._canvas.get_width()) if i % 2 == 0 else int(coeffs[i] * self._canvas.get_height())
                    for i in range(len(coeffs))]
        pg.draw.rect(self._canvas, colors["cyan"], pg.Rect(location[0], location[1], location[2], location[3]), 0,
                     10)  # cyan card outline
        pg.draw.rect(self._canvas, colors["blue"],
                     pg.Rect(location[0] + border, location[1] + border, location[2] - 2 * border, location[3] - 2 * border), 0,
                     10)  # blue backing
        self._canvas.blit(text, textRect)  # name of city on top of discard

        # Draw player discard
        if len(self.player_discard) > 0:
            text_color = tuple([255 - val for val in colors[self.player_discard[-1].display_color]])
            text = font.render(self.player_discard[-1].name, True,
                               text_color)
            textRect = text.get_rect()
            textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.13) * self._canvas.get_width()),
                               int((coeffs[1] + (coeffs[3] / 2)) * self._canvas.get_height())]
            location = [int(coeffs[i] * self._canvas.get_width()) if i % 2 == 0 else int(coeffs[i] * self._canvas.get_height())
                        for i in range(len(coeffs))]
            pg.draw.rect(self._canvas,
                         colors["white"],
                         pg.Rect(location[0] + offset,
                                 location[1],
                                 location[2],
                                 location[3]),
                         0,
                         10)  # white card outline
            pg.draw.rect(self._canvas,
                         colors[self.player_discard[-1].display_color],
                         pg.Rect(location[0] + border + offset,
                                 location[1] + border,
                                 location[2] - 2 * border,
                                 location[3] - 2 * border),
                         0,
                         10)  # backing matches city color
            self._canvas.blit(text, textRect)  # name of card on top of discard

            text = font.render(str(len(self._player_discard)), True, text_color)
            textRect = text.get_rect()
            textRect.center = [int((coeffs[0] + (coeffs[2] / 2) + 0.1) * self._canvas.get_width()),
                               int((coeffs[1] + (coeffs[3] / 2) - 0.07) * self._canvas.get_height())]

            self._canvas.blit(text, textRect)

    # ----------------------------------------- HELPER METHODS --------------------------------------------------------
    def city_list(self) -> List[City]:
        return sorted(list(self.cities.values()))

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

    def emergency_path(self, start_city_name: str) -> list:
        """Find the shortest path between two cities using BFS."""
        if start_city_name not in self._cities.keys():
            raise ValueError("The specified city does not exist.")

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
            if sum(current_city._disease_cubes.values()) >= 3:
                return path

            # Add neighbors to the queue
            for neighbor in current_city.neighbors:
                if neighbor.name not in visited:
                    queue.append((neighbor, path + [neighbor.name]))

        # Return an empty list if there is no path
        return []
