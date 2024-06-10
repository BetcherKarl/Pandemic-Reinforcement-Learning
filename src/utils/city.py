"""The file contains the city class for a game of Pandemic."""
from .color import Color

class City:
    """A class to represent a city in the game of Pandemic."""
    def __init__(self, name: str, color: Color, population: int):
        """Initialize a city with a name, color, and population."""
        if name:
            self._name = name
        if color.name in ["blue", "yellow", "black", "red"]:
            self._color = color
        else:
            raise ValueError(f"Invalid color for city {name}: {color}\n Valid colors are: blue, yellow, black, red.")
        if population > 100000:
            self._population = population
        else:
            raise ValueError(f"Invalid population for city {name}: {population}\n Population must be greater than 100,000.")
        self._disease_cubes = {'blue': 0, 'yellow': 0, 'black': 0, 'red': 0}
        self._research_station = False
        self._neighbors = []

        self._outbroken = False

        # Quarantine Specialist logic
        self._quarantined = False

        self._position = [0.0, 0.0]


    def __str__(self):
        """Return the name of the city."""
        return self._name
    
    def __repr__(self):
        """Return a representation of the city."""
        return f"City(name='{self._name}', color='{self._color}', population={self._population}, disease_cubes={self._disease_cubes}, research_station={self._research_station}, neighbors={self._neighbors})"

    @property
    def name(self) -> str:
        """Return the name of the city."""
        return self._name

    @name.setter
    def name(self, other: str):
        """Set the name of the city."""
        self._name = other

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, other: Color):
        """Set the color of the city."""
        self._color = other

    @property
    def population(self) -> int:
        """Return the population of the city."""
        return self._population

    @population.setter
    def population(self, other: int):
        """Set the population of the city."""
        if other > 100000:
            self._population = other
        else:
            raise ValueError(f"New population value of {other} is not valid for city {self.name}."
                             f"\nCity population must be greater than 100,000.")

    @property
    def disease_cubes(self):
        """Return the disease cubes for the city."""
        return self._disease_cubes

    @disease_cubes.setter
    def disease_cubes(self, other:dict[Color, int]) -> None:
        self._disease_cubes = other

    @property
    def position(self):
        """Return the position of the city on the screen"""
        return self._position

    @position.setter
    def position(self, other:list[float, float]) -> None:
        if len(other) != 2:
            raise ValueError(f"Invalid length of {len(other)} position for city {self._name}.\n"
                             f"Position is a list of two percentages, in decimal form.")
        elif not isinstance(other[0], float) or not isinstance(other[1], float):
            raise TypeError(f"Invalid type for entries of position: {type(other[0])} and {type(other[1])} for city {self._name}.\n"
                            f"Position is a list of two percentages, in decimal form.")
        elif not 0 <= other[0] <= 1 or not 0 <= other[1] <= 1:
            raise ValueError(f"Invalid value for positions {other[0]} and {other[1]} for city {self._name}.\n"
                             f"Position values must be decimals between 0 and 1.")
        else:
            self._position = other
    
    @property
    def neighbors(self) -> list:
        """Return the neighbors of the city."""
        return self._neighbors

    @neighbors.setter
    def neighbors(self, other: list) -> None:
        self._neighbors = other

    @property
    def has_research_station(self) -> bool:
        return self._research_station

    @has_research_station.setter
    def has_research_station(self, other: bool) -> None:
        self._research_station = bool(other)
    
    def add_neighbor(self, neighbor):
        """Add a neighbor to the city."""
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.add_neighbor(self)

    def infect(self, color: str, num_cubes: int=1) -> False:
        """Infect the city with a number of disease cubes of a given color."""
        if not self._quarantined and not self._color.eradicated:
            if num_cubes < 0:
                raise ValueError(f"Number of disease cubes must be greater than 0.")
            elif num_cubes > 3:
                raise ValueError(f"Number of disease cubes must be less than 4.")

            if not color:
                color = self._color.name
            if color in self.disease_cubes.keys():
                if self.disease_cubes[color] + num_cubes > 3:
                    print(f"Oh no, an outbreak at {self.name}")
                    if not self._outbroken:
                        self._outbroken = True
                        self.disease_cubes[color] = 3
                        num_outbreaks = 0
                        for city in self.neighbors:
                            num_outbreaks += city.infect(color, 1)
                            self._outbroken = False
                        return num_outbreaks + 1
                else:
                    self.disease_cubes[color] += num_cubes
                    return 0
            else:
                raise ValueError(f"Invalid disease color: {color}\nValid colors are: blue, yellow, black, red.")
