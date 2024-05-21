"""The file containing the player card class for a game of Pandemic."""
from abc import ABC, abstractmethod


class PlayerCard(ABC):
    def __init__(self, board):
        """Initialize a player card with a board."""
        self._board = board
        self._name = None
        self._display_color = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def display_color(self) -> str:
        return self._display_color

    def use(self, player):
        """Use the card."""
        pass


class CityCard(PlayerCard):
    """A class to represent a city card in the game of Pandemic."""

    def __init__(self, board, city):
        """Initialize a city card with a city."""
        super().__init__(board)
        self._city = city
        self._color = city.color
        self._name = city.name

    @property
    def color(self):
        """Return the color of the city."""
        return self._color

    @property
    def city(self):
        """Return the city of the city card."""
        return self._city

    @property
    def display_color(self) -> str:
        return self._color.name

    def __str__(self):
        """Return the name of the city."""
        return self._city.name

    def __repr__(self):
        """Return a representation of the city card."""
        return f"CityCard(city={self._city})"

    def use(self, player) -> int:
        """Discard this card to use it.
        
        When a player discards a city card, they may move to the city on the card.
        If they are on the city on the card, they may go to any city on the map."""
        if self._city != player.location:
            player.location = self._city
        else:
            raise NotImplementedError("Choose a city to move to.")  # TODO: Requires player input

        return 1  # Actions return their cost


class EpidemicCard(PlayerCard):
    """A class to represent an epidemic card in the game of Pandemic."""

    def __init__(self, board):
        """Initialize an epidemic card."""
        super().__init__(board)
        self._name = 'Epidemic'
        self._display_color = 'green'


    def __str__(self):
        """Return the name of the card."""
        return "Epidemic"

    def __repr__(self):
        """Return a representation of the epidemic card."""
        return "EpidemicCard()"


class EventCard(PlayerCard, ABC):
    def __init__(self, board):
        super().__init__(board)
        self._name = None
        self._display_color = 'amber'

    def use(self, player):
        """Use the event card."""
        return 0  # Actions return their cost


class Airlift(EventCard):
    def __init__(self, board):
        super().__init__(board)
        self._name = 'Airlift'


    def use(self, player):
        pass


class Forecast(EventCard):
    def __init__(self, board):
        super().__init__(board)
        self._name = 'Forecast'


    def use(self, player):
        pass


class GovernmentGrant(EventCard):
    def __init__(self, board):
        super().__init__(board)
        self._name = 'Government Grant'


class OneQuietNight(EventCard):
    def __init__(self, board):
        super().__init__(board)
        self._name = 'One Quiet Night'


    def use(self, player):
        """Skip the next infect cities step."""
        self._board.quiet_night = True
        super().use()


class ResilientPopulation(EventCard):
    def __init__(self, board):
        super().__init__(board)
        self._name = 'Resilient Population'

