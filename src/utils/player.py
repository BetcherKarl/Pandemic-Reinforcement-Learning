"""This file contains the player class fo * (board_size / 0.65)r a game of Pandemic."""
from .color import Color
from .city import City
from .card import PlayerCard, CityCard, EventCard
from abc import ABC, abstractmethod

from time import sleep
from math import factorial
import logging


class Player(ABC):
    """An agent in a game of pandemic."""
    def __init__(self, board, starting_city):
        """Initialize a player with a role and a hand of cards."""
        # self.canvas = canvas
        self._score = 0
        self.action_limit = 4
        self.actions_remaining: int = self.action_limit
        self.actions = {
            'drive/ferry': self.drive_ferry,
            'treat disease': self.treat_disease,
            'place research station': self.place_research_station,
            'shuttle flight': self.shuttle_flight,
            'card movement': self.use_card,
            'share knowledge': self.share_knowledge,
            'discover a cure': self.discover_a_cure
        } # TODO: Implement action logic
        self.board = board
        self._hand: list[PlayerCard] = []
        self.location: City = board.cities[starting_city]
        self.hand_limit = 7

    @property
    @abstractmethod
    def pawn_color(self) -> str:
        pass

    @property
    def hand(self):
        """Return the hand of the player"""
        return self._hand

    @hand.setter
    def hand(self, other):
        self._hand = other

    @property
    @abstractmethod
    def role(self):
        pass

    def add_to_hand(self, card):
        """Add a card to the player's hand."""
        self.hand.append(card)
        self.hand.sort(key=lambda x: x.name)
        self.hand.sort(key=lambda x: x.color)
        if len(self.hand) > self.hand_limit:
            raise NotImplementedError("Hand limit reached.") # TODO: Implement discard logic

    def discover_a_cure(self, cards_to_cure: int = 5) -> int:  # TODO: Test this
        """Cure a disease of a certain color."""
        if self.location.research_station:
            card_counter = {color: 0 for color in self.board.colors.keys()}
            for card in self.hand:
                if isinstance(card, CityCard):
                    card_counter[card.color] += 1

            color = max(card_counter, key=card_counter.get)
            if card_counter[color] >= cards_to_cure:
                self.board.cured[color] = True
                if all([board_color.cured for board_color in self.board.colors.values()]):
                    self.board.win()
                    return 1000 # game won!

                return 250 # big reward for getting closer to winning the game
            else:
                return -1 * (5 - card_counter[color]) # invalid action
                # warn
        else:
            return -10 # invalid action
            raise ValueError("No research station in the current city.")

    def drive_ferry(self, city: City) -> int: # TODO: Implement logic for moving to a city
        """Move to a city connected by a white line."""
        if city in self.location.neighbors:
            self.location = city
            return 0
        else:
            return -1 # invalid action
            raise ValueError(f"{city} is not a neighbor of {self.location}.")

    def go_to(self, city: City) -> None:
        print(f"Player {self.role} is going to {city.name}.")
        path = self.board.shortest_path(self.location.name, city.name)
        for stop in path[1:]:
            print(f"\tPlayer {self.role} is moving to {stop}.")
            sleep(2)
            self.drive_ferry(self.board.cities[stop])

    def save_the_day(self, wait_time=2) -> None:
        path = self.board.emergency_path(self.location.name)
        print(f"Player {self.role} is going to {path[-1]}.")
        for stop in path[1:]:
            print(f"\tPlayer {self.role} is moving to {stop}.")
            sleep(wait_time)
            # self.take_action['drive/ferry'](self.board.cities[stop])
            self.take_action('drive/ferry', arg=self.board.cities[stop])
        sleep(wait_time)
        while self.location.disease_cubes[self.location.color.name] > 0:
            self.take_action('treat disease')
            sleep(wait_time)

    def place_research_station(self) -> int: # TODO: Test this
        """Place a research station in the current city."""
        if self.location.has_research_station:
            return -1 # invalid action
            raise ValueError(f"There is already a research station in {self.location.name}, "
                             f"{self.role} is attempting to place one here")
        for card in self.hand:
            if isinstance(card, CityCard):
                if card.city == self.location:
                    self.location.has_research_station = True
                    return 5
        return -3 # invalid action
        raise ValueError(f"Player {self.role} is missing card to place research station in city {self.location.name}")

    def shuttle_flight(self, city: City) -> int: # TODO: Test this
        """Move to a city with a research station."""
        if self.location.research_station and city.research_station:
            self.location = city
            return 2
        elif city.research_station:
            return -1 # invalid action
            raise ValueError(f"{city} does not have a research station.")
        else:
            return -2 # invalid action
            raise ValueError(f"{self.location} does not have a research station.")

    def state(self) -> np.Array:
        city_list = board.city_list()
        state = board.state()
        i = 0
        for card in self.hand:
            if isinstance(card, EventCard):
                state.append(-1)
            else:
                state.append(city_list.index(card.city))
            i += 1
        while i < 7:
            state.append(0)
            i += 1
        raise NotImplementedError("Add all players hands to the state."
                                  "Consider adding extra input nuerons for each card's color????")
        return np.Array(state)

    def take_action(self, action: str, arg=None) -> None:
        """Take an action from the player's action list."""
        if action in self.actions.keys():
            if arg is None:
                self.actions_remaining -= 1
                reward = self.actions[action]() # actions return their reward
            else:
                self.actions_remaining -= 1
                reward = self.actions[action](arg)  # actions return their reward
            self._score += reward
        else:
            raise ValueError(f"Invalid action: {action}")

    def treat_disease(self, cube_color: int) -> int:
        """Treat the disease in the current city.

        :param cube_color: The index of the color of cubes to remove
        """
        if not 0 <= cube_color <= 3:
            return -20  # invalid action
        color = self.board.colors.keys[cube_color]
        if self.location.disease_cubes[color] > 0:
            if self.location.color.cured:
                reward = (self.location.disease_cubes[color] * (self.location.disease_cubes[color] + 1)) / 2
                print(f"Player {self.role} is removing all disease cubes at {self.location.name}")
                self.location.color.disease_cubes += self.location.disease_cubes[color]
                self.location.disease_cubes[color] = 0
                if self.board.colors[color].disease_cubes == 24:
                    self.location.color.eradicate()
                    reward += 100
            else:
                reward = self.location.disease_cubes[color]
                self.location.color.disease_cubes += 1
                self.location.disease_cubes[self.location.color.name] -= 1
                print(f"Player {self.role} is removing a disease cube at {self.location.name}")
            if not any([self.location.name == card.name for card in self.board.infection_discard]):
                reward *= 2  # bonus reward if card is yet to be drawn from infection deck
            return reward
        return -10  # invalid action

    def turn_end(self):
        """End the player's turn."""
        self.board.next_player()

    def turn_start(self):
        """Start the player's turn."""
        pass
        
    def use_card(self, index: int) -> int:
        """Use a card from the player's hand."""
        reward = self.hand.pop(index).use(self)
        return reward
    
    def share_knowledge(self, player) -> int:
        """Give or take a city card from another player."""
        self_card_counter = {color: 0 for color in self.board.colors.keys()}
        player_card_counter = {color: 0 for color in self.board.colors.keys()}

        for card in self.hand:
            if isinstance(card, CityCard):
                self_card_counter[card.color] += 1

        for card in player.hand:
            if isinstance(card, CityCard):
                player_card_counter[card.color] += 1



        if player.role == "Researcher":
            raise NotImplementedError("Researcher logic not implemented.")
        if self.location == player.location:
            for card in player.hand:
                try:
                    if card.city == self.location:
                        self.add_to_hand(card)
                        player.hand.remove(card)
                        return  player_card_counter[card.color] ** 2

                except AttributeError:
                    pass
            for card in self.hand:
                try:
                    if card.city == self.location:
                        player.add_to_hand(card)
                        self.hand.remove(card)
                        return self_card_counter[card.color] ** 2
                except AttributeError:
                    pass
            return -5
        return -10


class ContingencyPlanner(Player): # TODO: Implement this
    """A player with the contingency planner role."""
    def __init__(self, board, starting_city):
        """Initialize a contingency planner player."""
        super().__init__(board, starting_city)
        self.special_event = None

    @property
    def pawn_color(self) -> str:
        return "cyan"

    @property
    def role(self) -> str:
        return 'Contingency Planner'

    def special_action(self) -> int:
        if self.special_event is not None:
            return -10
        cards = []
        for card in self.board.player_discard:
            if isinstance(card, EventCard):
                cards.append(card)

        if len(cards) > 0:
            raise NotImplementedError("Implement choice")
            choice: EventCard
            # self.board.player_discard.
        else:
            raise ValueError("No applicable cards")


class Dispatcher(Player): # TODO: Implement this
    """A player with the dispatcher role."""
    def __init__(self, board, starting_city):
        """Initialize a dispatcher player."""
        super().__init__(board, starting_city)

    @property
    def pawn_color(self) -> str:
        return "pink"

    @property
    def role(self):
        return 'Dispatcher'

    def special_action(self) -> int:
        raise NotImplementedError("Implement Dispatcher movement")


class OperationsExpert(Player):  # TODO: Implement this
    """A player with the operations expert role."""
    def __init__(self, board, starting_city):
        """Initialize an operations expert player."""
        super().__init__(board, starting_city)

    @property
    def pawn_color(self) -> str:
        return "lime"

    @property
    def role(self):
        return 'Operations Expert'

    def special_action(self) -> int:
        raise NotImplementedError("Implement Operations Expert action")
        return 10


class Medic(Player): # TODO: Test this
    # TODO: Find a better implementation of the Medic's ability to auto-remove stuff using quarantine logic (may have to change bool to int)
    """A player with the medic role."""
    def __init__(self, board, starting_city):
        """Initialize a medic player."""
        super().__init__(board, starting_city)

    @property
    def pawn_color(self) -> str:
        return "orange"

    @property
    def role(self) -> str:
        return 'Medic'

    def treat_disease(self, cube_color:int) -> int:
        """Treat the disease in the current city."""
        raise NotImplementedError("cube_color parameter not implemented. Reference player base class's treat_disease function")
        if self.location.disease_cubes[self.location.color.name] > 0:
            print(f"Player medic is removing all disease cubes at {self.location.name}")
            num_cubes = self.location.disease_cubes[self.location.color.name]
            self.location.disease_cubes[self.location.color.name] = 0
            self.location.color.disease_cubes += num_cubes
        else:
            raise ValueError(f"City {self.location.name} does not have disease cubes. Player Medic is attempting to remove cubes")

    def take_action(self, action: str, arg=None) -> None:
        """Take an action from the player's action list."""
        super().take_action(action, arg=arg)
        current_color = self.board._colors[self.location.color.name]
        if current_color.cured and not current_color.eradicated:
            raise NotImplementedError("Reward function for Medic auto-treating not implemented")
            reward += self.treat_disease()

    def turn_start(self):
        if any([player.role == 'Quarantine Specialist' for player in self.board.players]):
            counter = 0
            while self.board.players[counter].role != 'Quarantine Specialist':
                counter += 1
            quarantine_specialist = self.board.players[counter]
            if not quarantine_specialist.location.name in self.location.neighbors:
                self.location.quarantined = False
        else:
            self.location.quarantined = False
        super().turn_start()

    def turn_end(self):
        if self.location.color.cured:
            self.location.quarantined = True
        super().turn_end()


class QuarantineSpecialist(Player): # TODO: Test this
    """A player with the quarantine specialist role."""
    def __init__(self, board, starting_city):
        """Initialize a quarantine specialist player."""
        super().__init__(board, starting_city)

    @property
    def pawn_color(self) -> str:
        return "green"

    @property
    def role(self):
        return 'Quarantine Specialist'

    def turn_start(self):
        """Start the player's turn."""
        # clear all quarantines
        self.location.quarantined = False
        for city in self.location.neighbors:
            city.quarantined = False
        super().turn_start()

    def turn_end(self):
        """End the player's turn."""
        # quarantine all neighbors, they cannot have cubes placed on them
        raise NotImplementedError("Reward function for quarantine specialist's end turn placement not implemented")
        self.location.quarantined = True
        for city in self.location.neighbors:
            board.cities[city].quarantined = True
        super().turn_end()


class Researcher(Player): # TODO: Test this
    """A player with the researcher role."""
    def __init__(self, board, starting_city):
        """Initialize a researcher player."""
        super().__init__(board, starting_city)

    @property
    def pawn_color(self) -> str:
        return "brown"

    @property
    def role(self):
        return 'Researcher'

    def share_knowledge(self, player) -> int:
        raise NotImplementedError("Trading cards with researcher not implemented")


class Scientist(Player): # TODO: Test this
    """A player with the scientist role."""
    def __init__(self, board, starting_city):
        """Initialize a scientist player."""
        super().__init__(board, starting_city)

    @property
    def pawn_color(self) -> str:
        return "white"

    @property
    def role(self) -> str:
        return 'Scientist'

    def discover_a_cure(self, cards_to_cure: int = 4) -> int:
        """Cure a disease of a certain color."""
        reward = super().discover_a_cure(cards_to_cure)
        return reward