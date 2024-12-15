import unittest
from color import Color

class TestColor(unittest.TestCase):

    def setUp(self):
        self.color = Color(color='red')

    def test_disease_cubes_getter(self):
        self.assertEqual(self.color.disease_cubes, 24)

    def test_disease_cubes_setter(self):
        self.color.disease_cubes = 5
        self.assertEqual(self.color.disease_cubes, 5)
        self.color.eradicated = True
        self.color.disease_cubes = 10
        self.assertEqual(self.color.disease_cubes, 5)  # Should not change because eradicated is True

    def test_str(self):
        self.assertEqual(str(self.color), repr(self.color))

    def test_repr(self):
        expected_repr = "Color(color='red', disease_cubes=24, cured=False, eradicated=False)"
        self.assertEqual(repr(self.color), expected_repr)

    def test_hash(self):
        self.assertEqual(hash(self.color), hash('red'))

    def test_cure(self):
        self.color.cure()
        self.assertTrue(self.color.cured)

    def test_eradicate(self):
        self.color.cured = True
        self.color.disease_cubes = 24
        self.color.eradicate()
        self.assertTrue(self.color.eradicated)

if __name__ == '__main__':
    unittest.main()