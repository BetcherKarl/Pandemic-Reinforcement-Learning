"""File containing the color class for a disease color in the game of Pandemic."""
class Color:
    def __init__(self, color: str):
        """Initialize a color with a name."""
        if color in ["blue", "yellow", "black", "red"]:
            self._name = color
        else:
            raise ValueError(f"Invalid color: {color}\n Valid colors are: blue, yellow, black, red.")
        self.disease_cubes = 24
        self.cured = False
        self.eradicated = False

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        """Return the color of the disease."""
        return repr(self)
    
    def __repr__(self) -> str:
        """Return a representation of the color."""
        return f"Color(color='{self.name}', disease_cubes={self.disease_cubes}, cured={self.cured}, eradicated={self.eradicated})"
    
    def __hash__(self) -> int:
        """Return the hash of the color."""
        return hash(self.name)
    
    def cure(self) -> None:
        """Cure the disease."""
        self.cured = True

    def eradicate(self) -> None:
        """Eradicate the disease."""
        if self.disease_cubes == 24 and self.cured:
            self.eradicated = True