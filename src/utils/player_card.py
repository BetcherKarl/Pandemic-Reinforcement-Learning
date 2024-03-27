"""The file containing the player card class for a game of Pandemic."""
from abc import ABC, abstractmethod
from .board import PandemicBoard
from .player import Player

class PlayerCard(ABC):
    def __init__(self, board: PandemicBoard):
        """Initialize a player card with a board."""
        self.board = board
    
    def use(self, player: Player):
        """Use the card."""
        pass

class CityCard(PlayerCard):
    """A class to represent a city card in the game of Pandemic."""
    def __init__(self, city):
        """Initialize a city card with a city."""
        self.city = city
        self.color = city.color

    @property
    def color(self):
        """Return the color of the city."""
        return self.color
    
    @property
    def city(self):
        """Return the city of the city card."""
        return self.city

    def __str__(self):
        """Return the name of the city."""
        return self.city.name
    
    def __repr__(self):
        """Return a representation of the city card."""
        return f"CityCard(city={self.city})"
    
    def use(self, player: Player) -> int:
        """Discard this card to use it.
        
        When a player discards a city card, they may move to the city on the card.
        If they are on the city on the card, they may go to any city on the map."""
        if self.city != player.location:
            player.location = self.city
        else:
            raise NotImplementedError("Choose a city to move to.") # TODO: Requires player input
        
        return 1 # Actions return their cost
    
class EpidemicCard(PlayerCard):
    """A class to represent an epidemic card in the game of Pandemic."""
    def __init__(self):
        """Initialize an epidemic card."""
        pass

    def __str__(self):
        """Return the name of the card."""
        return "Epidemic"
    
    def __repr__(self):
        """Return a representation of the epidemic card."""
        return "EpidemicCard()"
    
class EventCard(PlayerCard, ABC):
    def use(self, player: Player):
        """Use the event card."""
        return 0 # Actions return their cost

class Airlift(EventCard):
    raise NotImplementedError("Airlift is not yet implemented.")

class Forecast(EventCard):
    raise NotImplementedError("Forecast is not yet implemented.")

class GovernmentGrant(EventCard):
    raise NotImplementedError("GovernmentGrant is not yet implemented.")

class OneQuietNight(EventCard):
    def use(self):
        """Skip the next infect cities step."""
        self.board.quiet_night = True
        super().use()

class ResilientPopulation(EventCard):
    raise NotImplementedError("ResilientPopulation is not yet implemented.")