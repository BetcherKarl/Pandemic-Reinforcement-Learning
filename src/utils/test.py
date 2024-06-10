import unittest
import random

from ..constants import r_seed
from ..utils.board import PandemicBoard
from ..utils.city import City
from ..utils.color import Color
from ..utils.infection_card import InfectionCard
from ..utils.player import (ContingencyPlanner, Dispatcher, OperationsExpert, Medic,
                            QuarantineSpecialist, Researcher, Scientist)
from ..utils.player_card import CityCard, EpidemicCard, EventCard

random.seed(r_seed)

# TODO: Finish this file :)

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = PandemicBoard(r_seed=r_seed)

class CityTest(unittest.TestCase):
    def setUp(self) -> City:
        self.board = PandemicBoard(None)
        return random.choice(self.board.city_list())