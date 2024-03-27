"""This file contains the player class for a game of Pandemic."""

from .board import PandemicBoard
from .color import Color
from .player_card import PlayerCard, CityCard
from .city import City
from abc import ABC, abstractmethod

class Player(ABC):
    """An agent in a game of pandemic."""
    def __init__(self, board:PandemicBoard):
        """Initialize a player with a role and a hand of cards."""
        
        self.action_limit = 4
        self.actions_remaining = self.action_limit
        self.actions = {} # TODO: Implement action logic
        self.board = board
        self.hand = []
        self.location = board.cities["Atlanta"]
        self.hand_limit = 7
        self.pawn_color = None
        self.role = None

    def add_to_hand(self, card: PlayerCard) -> int:
        """Add a card to the player's hand."""
        self.hand.append(card)
        return 0 # actions return their action cost
        if len(self.hand) > self.hand_limit:
            raise NotImplementedError("Hand limit reached.") # TODO: Implement discard logic

    def drive_ferry(self, city: City) -> int: # TODO: Implement logic for moving to a city
        """Move to a city connected by a white line."""
        if city in self.location.neighbors:
            self.location = city
            return 1 # actions return their action cost
        else:
            raise ValueError(f"{city} is not a neighbor of {self.location}.")
        
    def cure_disease(self, cards_to_cure: int=5): # TODO: Test this
        """Cure a disease of a certain color."""
        if self.location.research_station:
            for card in self.hand:
                card_counter = {color: 0 for color in self.board.colors.values()}
                if isinstance(card, CityCard) and card.color in card_counter.keys():
                    card_counter[card.color] += 1
            color = max(card_counter, key=card_counter.get)
            if card_counter[color] >= cards_to_cure:
                self.board.cured[color] = True
                return 1 # actions return their action cost
            else:
                raise ValueError("Not enough cards to cure the disease.")
        else:
            raise ValueError("No research station in the current city.")

    def place_research_station(self, city: City): # TODO: Test this
        """Place a research station in the current city."""
        for card in self.hand:
            if isinstance(card, CityCard) and card.city == self.location:
                self.hand.remove(card)
                self.location.research_station = True
                return 1 # actions return their action cost

    def shuttle_flight(self, city: City): # TODO: Test this
        """Move to a city with a research station."""
        if self.location.research_station and city.research_station:
            self.location = city
            return 1
        else:
            raise ValueError(f"{city} does not have a research station.")
        
    def take_action(self, action: str):
        """Take an action from the player's action list."""
        if action in self.actions.keys():
            self.actions_remaining -= self.actions[action]() # actions return their action cost
        else:
            raise ValueError(f"Invalid action: {action}")

    def treat_city(self):
        """Treat the disease in the current city."""
        if self.location.disease_cubes[self.location.color] > 0:
            if self.location.color.cured:
                self.location.disease_cubes[self.location.color] = 0

    def turn_end(self):
        """End the player's turn."""
        self.board.draw_player_cards(self)
        self.board.infect_cities()
        self.actions_remaining = self.action_limit
        self.board.current_player = (self.board.current_player + 1) % len(self.board.players)

    def turn_start(self):
        """Start the player's turn."""
        pass
        
    def use_card(self, index: int):
        """Use a card from the player's hand."""
        self.hand.pop(index).use(self)
    
    def share_knowledge(self, player: Player, card: CityCard):
        """Give or take a city card from another player."""
        if player.role == "Researcher":
            raise NotImplementedError("Researcher logic not implemented.")
        if self.location == player.location:
            for card in player.hand:
                if isinstance(card, CityCard) and card.city == self.location:
                    self.hand.append(card)
                    player.hand.remove(card)
                    self.actions_remaining -= 1
                    return
            for card in self.hand:
                if isinstance(card, CityCard) and card.city == self.location:
                    player.hand.append(card)
                    self.hand.remove(card)
                    self.actions_remaining -= 1
                    return

class ContingencyPlanner(Player): # TODO: Implement this
    """A player with the contingency planner role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a contingency planner player."""
        super().__init__(board)
        self.role = 'Contingency Planner'
        self.special_event = None

class Dispatcher(Player): # TODO: Implement this
    """A player with the dispatcher role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a dispatcher player."""
        super().__init__(board)
        self.role = 'Dispatcher'

class OperationsExpert(Player): # TODO: Implement this
    """A player with the operations expert role."""
    def __init__(self, board:PandemicBoard):
        """Initialize an operations expert player."""
        super().__init__(board)
        self.role = 'Operations Expert'

class Medic(Player): # TODO: Test this
    """A player with the medic role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a medic player."""
        super().__init__(board)
        self.role = 'Medic'

    def treat_city(self):
        """Treat the disease in the current city."""
        if self.location.disease_cubes[self.location.color] > 0:
            num_cubes = self.location.disease_cubes[self.location.color]
            self.location.disease_cubes[self.location.color] = 0
            self.board.disease_cubes[self.location.color] += num_cubes
            self.actions_remaining -= 1

    def take_action(self, action: str):
        """Take an action from the player's action list."""
        for color in self.board.colors.values():
            if color.cured:
                self.location.disease_cubes[color] = 0
        super().take_action(action)

class QuarantineSpecialist(Player): # TODO: Test this
    """A player with the quarantine specialist role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a quarantine specialist player."""
        super().__init__(board)
        self.role = 'Quarantine Specialist'

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
        self.location.quarantined = True
        for city in self.location.neighbors:
            city.quarantined = True
        super().turn_end()

class Researcher(Player): # TODO: Test this
    """A player with the researcher role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a researcher player."""
        super().__init__(board)
        self.role = 'Researcher'

class Scientist(Player): # TODO: Test this
    """A player with the scientist role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a scientist player."""
        super().__init__(board)
        self.role = 'Scientist'

    def cure_disease(self):
        """Cure a disease of a certain color."""
        super().cure_disease(4)





