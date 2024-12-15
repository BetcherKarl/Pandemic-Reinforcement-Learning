import unittest
from color import Color
from city import City
from card import InfectionCard, CityCard, EpidemicCard, Airlift, Forecast, GovernmentGrant, OneQuietNight, ResilientPopulation

class TestInfectionCard(unittest.TestCase):

    def setUp(self):
        self.color = Color(color='red')
        self.city = City(name='Atlanta', color=self.color, population=500000)
        self.card = InfectionCard(board=None, city=self.city)

    def test_name(self):
        self.assertEqual(self.card.name, 'Atlanta')

    def test_color(self):
        self.assertEqual(self.card.color, 'red')

    def test_city(self):
        self.assertEqual(self.card.city, self.city)

class TestCityCard(unittest.TestCase):

    def setUp(self):
        self.color = Color(color='red')
        self.city = City(name='Atlanta', color=self.color, population=500000)
        self.card = CityCard(board=None, city=self.city)

    def test_name(self):
        self.assertEqual(self.card.name, 'Atlanta')

    def test_color(self):
        self.assertEqual(self.card.color, 'red')

    def test_city(self):
        self.assertEqual(self.card.city, self.city)

    def test_use(self):
        player = type('Player', (object,), {'location': None})()
        self.card.use(player)
        self.assertEqual(player.location, self.city)

class TestEpidemicCard(unittest.TestCase):

    def setUp(self):
        self.card = EpidemicCard(board=None)

    def test_name(self):
        self.assertEqual(self.card.name, 'Epidemic')

    def test_color(self):
        self.assertEqual(self.card.color, 'dark green')

class TestEventCards(unittest.TestCase):

    def test_airlift(self):
        card = Airlift(board=None)
        self.assertEqual(card.name, 'Airlift')

    def test_forecast(self):
        card = Forecast(board=None)
        self.assertEqual(card.name, 'Forecast')

    def test_government_grant(self):
        card = GovernmentGrant(board=None)
        self.assertEqual(card.name, 'Government Grant')

    def test_one_quiet_night(self):
        card = OneQuietNight(board=None)
        self.assertEqual(card.name, 'One Quiet Night')

    def test_resilient_population(self):
        card = ResilientPopulation(board=None)
        self.assertEqual(card.name, 'Resilient Population')

if __name__ == '__main__':
    unittest.main()