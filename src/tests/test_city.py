import unittest
from color import Color
from city import City

class TestCity(unittest.TestCase):

    def setUp(self):
        self.color = Color(color='red')
        self.city = City(name='Atlanta', color=self.color, population=500000)

    def test_name_getter(self):
        self.assertEqual(self.city.name, 'Atlanta')

    def test_name_setter(self):
        self.city.name = 'Chicago'
        self.assertEqual(self.city.name, 'Chicago')

    def test_color_getter(self):
        self.assertEqual(self.city.color, self.color)

    def test_color_setter(self):
        new_color = Color(color='blue')
        self.city.color = new_color
        self.assertEqual(self.city.color, new_color)

    def test_population_getter(self):
        self.assertEqual(self.city.population, 500000)

    def test_population_setter(self):
        self.city.population = 600000
        self.assertEqual(self.city.population, 600000)
        with self.assertRaises(ValueError):
            self.city.population = 50000

    def test_disease_cubes_getter(self):
        self.assertEqual(self.city.disease_cubes, {'blue': 0, 'yellow': 0, 'black': 0, 'red': 0})

    def test_disease_cubes_setter(self):
        new_cubes = {'blue': 1, 'yellow': 2, 'black': 3, 'red': 4}
        self.city.disease_cubes = new_cubes
        self.assertEqual(self.city.disease_cubes, new_cubes)

    def test_position_getter(self):
        self.assertEqual(self.city.position, [0.0, 0.0])

    def test_position_setter(self):
        new_position = [0.5, 0.5]
        self.city.position = new_position
        self.assertEqual(self.city.position, new_position)
        with self.assertRaises(ValueError):
            self.city.position = [0.5]
        with self.assertRaises(TypeError):
            self.city.position = [0.5, '0.5']
        with self.assertRaises(ValueError):
            self.city.position = [1.5, 0.5]

    def test_neighbors_getter(self):
        self.assertEqual(self.city.neighbors, [])

    def test_neighbors_setter(self):
        new_neighbors = ['Chicago', 'Miami']
        self.city.neighbors = new_neighbors
        self.assertEqual(self.city.neighbors, new_neighbors)

    def test_has_research_station_getter(self):
        self.assertFalse(self.city.has_research_station)

    def test_has_research_station_setter(self):
        self.city.has_research_station = True
        self.assertTrue(self.city.has_research_station)

    def test_add_neighbor(self):
        neighbor_city = City(name='Chicago', color=self.color, population=500000)
        self.city.add_neighbor(neighbor_city)
        self.assertIn(neighbor_city, self.city.neighbors)
        self.assertIn(self.city, neighbor_city.neighbors)

    def test_infect(self):
        self.city.infect('red', 1)
        self.assertEqual(self.city.disease_cubes['red'], 1)
        with self.assertRaises(ValueError):
            self.city.infect('red', -1)
        with self.assertRaises(ValueError):
            self.city.infect('red', 4)

if __name__ == '__main__':
    unittest.main()