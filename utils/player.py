"""This file contains the player class for a game of Pandemic."""

from .board import PandemicBoard
from .player_card import PlayerCard
from .city import City
from abc import ABC, abstractmethod

class HandLimitReached(Exception):
    """An exception for when a player's hand limit is reached."""
    def __init__(self, player):
        """Initialize the exception with a player."""
        self.player = player
        super().__init__(f"{player} has reached their hand limit.")

class Player(ABC):
    """An agent in a game of pandemic."""
    def __init__(self, board:PandemicBoard):
        """Initialize a player with a role and a hand of cards."""
        
        self.action_limit = 4
        self.actions = {"Drive/Ferry": self.drive_ferry,
                        "Direct Flight": self.direct_flight,
                        "Charter Flight": self.charter_flight,
                        "Shuttle Flight": self.shuttle_flight,
                        "Build Research Station": self.build_research_station,
                        "Treat Disease": self.treat_disease,
                        "Share Knowledge": self.share_knowledge,
                        "Discover Cure": self.discover_cure}
        self.board = board
        self.hand = []
        self.location = board.cities["Atlanta"]
        self.hand_limit = 7
        self.pawn_color = None
        self.role = None

    def add_to_hand(self, card: PlayerCard):
        """Add a card to the player's hand."""
        self.hand.append(card)
        if len(self.hand) > self.hand_limit:
            raise NotImplementedError("Hand limit reached.") # TODO: Implement discard logic
        
    def use_card(self, index: int):
        """Use a card from the player's hand."""
        self.hand.pop(index).use(self)
        


class ContingencyPlanner(Player):
    """A player with the contingency planner role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a contingency planner player."""
        super().__init__(board)
        self.role = 'Contingency Planner'
        self.special_event = None


class Dispatcher(Player):
    """A player with the dispatcher role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a dispatcher player."""
        super().__init__(board)
        self.role = 'Dispatcher'

class OperationsExpert(Player):
    """A player with the operations expert role."""
    def __init__(self, board:PandemicBoard):
        """Initialize an operations expert player."""
        super().__init__(board)
        self.role = 'Operations Expert'

class Medic(Player):
    """A player with the medic role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a medic player."""
        super().__init__(board)
        self.role = 'Medic'

class QuarantineSpecialist(Player):
    """A player with the quarantine specialist role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a quarantine specialist player."""
        super().__init__(board)
        self.role = 'Quarantine Specialist'

class Researcher(Player):
    """A player with the researcher role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a researcher player."""
        super().__init__(board)
        self.role = 'Researcher'

class Scientist(Player):
    """A player with the scientist role."""
    def __init__(self, board:PandemicBoard):
        """Initialize a scientist player."""
        super().__init__(board)
        self.role = 'Scientist'





