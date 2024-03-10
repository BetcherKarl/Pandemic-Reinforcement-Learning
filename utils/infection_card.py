"""This file contains the infection card class for a game of Pandemic."""

from .color import Color
from .city import City

class InfectionCard:
    def __init__(self, city: City):
        """Initialize an infection card with a city and color."""
        self.city = city
        self.color = city.color