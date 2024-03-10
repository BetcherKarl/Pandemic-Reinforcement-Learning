"""The file contains the city class for a game of Pandemic."""
from .color import Color

class City:
    """A class to represent a city in the game of Pandemic."""
    def __init__(self, name: str, color: Color, population: int):
        """Initialize a city with a name, color, and population."""
        if name:
            self.name = name
        if color in ["blue", "yellow", "black", "red"]:
            self.color = color
        else:
            raise ValueError(f"Invalid color for city {name}: {color}\n Valid colors are: blue, yellow, black, red.")
        if population > 100000:
            self.population = population
        else:
            raise ValueError(f"Invalid population for city {name}: {population}\n Population must be greater than 100,000.")
        self.disease_cubes = {Color('blue'): 0, Color('yellow'): 0, Color('black'): 0, Color('red'): 0}
        self.research_station = False
        self.neighbors = {}


    def __str__(self):
        """Return the name of the city."""
        return self.name
    
    def __repr__(self):
        """Return a representation of the city."""
        return f"City(name='{self.name}', color='{self.color}', population={self.population}, disease_cubes={self.disease_cubes}, research_station={self.research_station}, neighbors={self.neighbors})"
    
    @property
    def disease_cubes(self):
        """Return the disease cubes for the city."""
        return self.disease_cubes
    
    @property
    def neighbors(self):
        """Return the neighbors of the city."""
        return self.neighbors
    

    
    def add_neighbor(self, neighbor):
        """Add a neighbor to the city."""
        if neighbor.name not in self.neighbors.keys():
            self.neighbors[neighbor.name] = neighbor
            neighbor.add_neighbor(self)

    # def infect(self, color: Color, )
