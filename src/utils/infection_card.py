"""This file contains the infection card class for a game of Pandemic."""

from .color import Color
from .city import City

class InfectionCard:
    def __init__(self, city: City):
        """Initialize an infection card with a city and color."""
        self._city = city
        self._color = city.color

    def __str__(self):
        return self._city.__str__()

    @property
    def color(self):
        """Return the color of the infection card."""
        return self._color

    @property
    def city(self):
        """Return the city of the infection card."""
        return self._city

