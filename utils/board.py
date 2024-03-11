from .city import City
from .color import Color
from .player_card import CityCard, EpidemicCard, EventCard
from .player import Player, ContingencyPlanner, Dispatcher, Medic, OperationsExpert, QuarantineSpecialist, Researcher, Scientist
from .infection_card import InfectionCard

import random
import json

class PandemicBoard:
    def __init__(self, num_epidemics=5, num_players=3):
        """Initialize the board for Pandemic.
        Contains all the steps of setup in the Pandemic Rules"""

        self.score = 0 # The score to evaluate the Reinforcement Learning model
        # TODO: Implement the score system

        # STEP 0: Create the basic game components
        colors = {"blue": Color("blue"), "yellow": Color("yellow"), "black": Color("black"), "red": Color("red")}
        self.cities = {}
        self.create_cities()

        self.connections = [] # connections between cities
        for city_name, city in self.cities.items():
            for neighbor in self.cities[city].neighbors:
                order = tuple(sorted([city.location, neighbor.location]))
                if order not in self.connections:
                    self.connections.append(order)


        if num_epidemics in [4, 5, 6, 7]:
            self.total_epidemics = num_epidemics
        else:
            raise ValueError("Invalid number of epidemics. Must be 4, 5, 6, or 7.")
        self.infection_rate = [2, 2, 2, 3, 3, 4, 4, 4]

        self.outbreaks_curr = 0
        self.outbreaks_max = 8

        self.epidemics_drawn = 0
        self.epidemics_total = num_epidemics

        self.players = []
        self.current_player = 0 # index of the current player in the players list
        self.create_players(num_players)

        self.player_deck = []
        self.player_discard = []
        self.create_player_deck()

        self.infection_deck = []
        self.infection_discard = []
        self.create_infection_deck()

        self.cities["Atlanta"].research_station = True

        # Tracks card mechanics
        self.quiet_night = False

    # ------------------------Properties------------------------
    @property
    def cities(self) -> dict:
        """Return the cities for the game."""
        return self.cities
    
    @cities.setter
    def cities(self, cities: dict) -> None:
        """Set the cities for the game."""
        self.cities = cities

    @property
    def connections(self) -> list[City]:
        """Return the game board for the game."""
        return self.connections

    @property
    def epidemics_drawn(self) -> int:
        """Return the number of epidemics drawn."""
        return self.epidemics_drawn
    
    @epidemics_drawn.setter
    def epidemics_drawn(self, num: int) -> None:
        """Set the number of epidemics drawn."""
        self.epidemics_drawn = num

    @property
    def epidemics_total(self) -> int:
        """Return the total number of epidemics."""
        return self.epidemics_total

    @property
    def infection_discard(self) -> list[InfectionCard]:
        """Return the infection discard pile for the game."""
        return self.infection_discard
    
    @infection_discard.setter
    def infection_discard(self, discard: list) -> None:
        """Set the infection discard pile for the game."""
        self.infection_discard = discard

    @property
    def player_discard(self) -> list[PlayerCard]:
        """Return the player discard pile for the game."""
        return self.player_discard
    
    @player_discard.setter
    def player_discard(self, discard: list) -> None:
        """Set the player discard pile for the game."""
        self.player_discard = discard

    @property
    def team_score(self) -> int:
        """Return the team score for the game."""
        return self.team_score

    @property
    def num_outbreaks(self) -> int:
        """Return the number of outbreaks in the game."""
        return self.num_outbreaks
    
    @num_outbreaks.setter
    def num_outbreaks(self, num: int) -> None:
        """Set the number of outbreaks in the game."""
        self.num_outbreaks = num

    @property
    def total_epidemics(self) -> int:
        """Return the total number of epidemics."""
        return self.total_epidemics
    
    @total_epidemics.setter
    def total_epidemics(self, num: int) -> None:
        """Set the total number of epidemics."""
        self.total_epidemics = num

    @property
    def infection_rate(self) -> int:
        """Return the infection rate for the game."""
        return self.infection_rate[self.epidemics_drawn]

    @property
    def players(self) -> list[Player]:
        """Return the players for the game."""
        return self.players
    
    @players.setter
    def players(self, players: list) -> None:
        """Set the players for the game."""
        self.players = players

    @property
    def state(self) -> list[int]: # TODO: Finish this method
        """Return the state of the game as a list of integers"""
        state = []
        for city in self.cities:
            state.append(sum(city.disease_cubes.values())
    @property
    def turns_remaining(self) -> int:
        """Return the number of turns remaining in the game."""
        return len(self.player_deck) // 2
    
    # ------------------------Methods------------------------

    # Create the game components
    def create_cities(self, starting_city: str="Atlanta") -> None:
        """Create the cities for the game."""
        with open("cities.json", "r") as file:
            cities = json.load(file)
        for city in cities:
            self.cities[city["name"]] = City(city["name"], self.colors[city["color"]], city["population"])
        for city in cities:
            for neighbor in city["neighbors"]:
                self.cities[city["name"]].add_neighbor(self.cities[neighbor])

        # add research station to starting city
        self.cities[starting_city].research_station = True

    def create_players(self, num_players: int) -> None:
        """Create the players for the game."""
        roles = [ContingencyPlanner(self), Dispatcher(self),
                Medic(self), OperationsExpert(self),
                QuarantineSpecialist(self), Researcher(self),
                Scientist(self)]
        random.shuffle(roles)
        self.players = roles[:num_players]

    def create_infection_deck(self) -> None:
        """Create the infection deck for the game."""
        for city in self.cities:
            self.infection_deck.append(InfectionCard(city))
        random.shuffle(self.infection_deck)

    def create_player_deck(self) -> None:
        """Create the player deck for the game."""
        # Create all the city and event cards
        for city in self.cities:
            self.player_deck.append(CityCard(city))
        event_cards = [Airlift(), Forecast(), GovernmentGrant(), OneQuietNight(), ResilientPopulation()]
        for card in event_cards:
            self.player_deck.append(card)
        
        # deal the player cards
        random.shuffle(self.player_deck)
        num_cards = 6 - len(self.players)
        for player in self.players:
            for _ in range(num_cards):
                player.add_to_hand(self.player_deck.pop())

        # determine player order (highest population city goes first)
        self.players.sort(key=lambda x: max(x.hand, key=lambda y: isinstance(y, CityCard)).city.population, reverse=True)
                
        # add the epidemic cards
        subdecks = [[EpidemicCard()] for _ in range(self.total_epidemics)]
        for i in range(len(self.player_deck)): # distributing the epidemic cards evenly across the player deck
            subdecks[i % self.total_epidemics].append(self.player_deck[i])

        for deck in subdecks: # shuffle each subdeck
            random.shuffle(deck)

        self.player_deck = [] # compile each subdeck into the player deck
        for deck in subdecks:
            self.player_deck += deck

    # Game mechanics
    def infect_city(self, num_cubes:int=1, card:InfectionCard=None) -> None: # TODO: Test this method for multiple outbreaks at once
        """Infect a city from the top of the infection deck."""
        if self.quiet_night:
            self.quiet_night = False
            return
        
        if not card:
            card = self.infection_deck.pop()
        color = card.color
        if color.disease_cubes < num_cubes:
            self.lose()
        elif card.city.infect(num_cubes, color): # infect the city (method returns True if an outbreak occurs)
                self.num_outbreaks += 1
                if self.num_outbreaks >= self.outbreaks_max:
                    self.lose()

    def draw_player_card(self, player:Player) -> None:
        """Draw a player card from the top of the player deck."""
        if len(self.player_deck) < 2:
            self.lose()
        for _ in range(2):
            card = self.player_deck.pop()
            if isinstance(card, EpidemicCard):
                self.epidemic()
                self.player_discard.append(card)
            else:
                player.add_to_hand(card)

    def draw_infections(self) -> None:
        """Draw the infections for the game."""
        for _ in range(self.infection_rate):
            self.infect_city(1)

    def epidemic(self) -> None:
        """Handle an epidemic in the game."""
        # Increase
        self.epidemics_drawn += 1

        # Infect
        bottom_card = self.infection_deck.pop(0)
        self.infect_city(card=bottom_card, num_cubes=3)

        if any([any([isinstance(card, ResilientPopulation) for card in player.hand]) for player in self.players]):
            raise NotImplementedError("Put option in for someone to play ResilientPopulation.")
        
        # Intensify
        for card in random.shuffle(self.infection_discard):
            self.infection_deck.insert(0, card)


    def lose(self):
        """Lose the game."""
        raise NotImplementedError("Losing the game is not yet implemented.")
