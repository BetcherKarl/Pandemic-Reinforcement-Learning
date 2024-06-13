from abc import ABC, abstractmethod

from .color import Color
from .city import City


class Card(ABC):
    def __init__(self, board):
        """Initialize the card"""
        self._board = board

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def color(self) -> str:
        pass

    def __str__(self):
        return self.name


class InfectionCard(Card):
    def __init__(self, board, city: City):
        """Initialize an infection card with a city and color."""
        super().__init__(board)
        self._city = city
        self._color = city.color.name

    @property
    def name(self) -> str:
        return self._city.name

    @property
    def color(self):
        """Return the color of the infection card."""
        return self._color

    @property
    def city(self):
        """Return the city of the infection card."""
        return self._city


class PlayerCard(Card, ABC):
    def __init__(self, board):
        """Initialize a player card with a board."""
        super().__init__(board)

    @abstractmethod
    def use(self, player):
        """Use the card."""


class CityCard(PlayerCard):
    """A class to represent a city card in the game of Pandemic."""

    def __init__(self, board, city):
        """Initialize a city card with a city."""
        super().__init__(board)
        self._city = city

    @property
    def name(self):
        return self._city.name

    @property
    def color(self) -> str:
        """Return the color of the city."""
        return self.city.color.name

    @property
    def city(self):
        """Return the city of the city card."""
        return self._city

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

    @property
    def name(self):
        return 'Epidemic'

    @property
    def color(self) -> str:
        return "dark green"

    def __repr__(self):
        """Return a representation of the epidemic card."""
        return "EpidemicCard()"

    def use(self, player):
        pass


class EventCard(PlayerCard, ABC):
    def __init__(self, board):
        super().__init__(board)
        self._name = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> str:
        return "amber"

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
        super().use(player)


class ResilientPopulation(EventCard):
    def __init__(self, board):
        super().__init__(board)
        self._name = 'Resilient Population'