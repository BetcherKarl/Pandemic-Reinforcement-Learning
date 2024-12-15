import unittest
from unittest.mock import MagicMock
from board import PandemicBoard

class TestPandemicBoard(unittest.TestCase):

    def setUp(self):
        self.board = PandemicBoard(num_epidemics=5, num_players=3, starting_city="Atlanta")

    def test_create_cities(self):
        self.board.create_cities(starting_city="Atlanta")
        self.assertIn("Atlanta", self.board.cities)
        self.assertIn("Jakarta", self.board.cities)

    def test_create_players(self):
        self.board.create_players(num_players=3, starting_city="Atlanta")
        self.assertEqual(len(self.board.players), 3)

    def test_create_infection_deck(self):
        self.board.create_infection_deck()
        self.assertGreater(len(self.board._infection_deck), 0)

    def test_create_player_deck(self):
        self.board.create_player_deck()
        self.assertGreater(len(self.board._player_deck), 0)

    def test_infect_city(self):
        card = MagicMock()
        card.city = MagicMock()
        card.color = "red"
        self.board.infect_city(num_cubes=1, card=card)
        card.city.infect.assert_called_with("red", 1)

    def test_draw_player_cards(self):
        player = MagicMock()
        self.board._player_deck = ["card1", "card2"]
        self.board.draw_player_cards(player=player)
        self.assertEqual(len(self.board._player_deck), 0)

    def test_draw_infection_cards(self):
        self.board._infection_deck = ["card1", "card2"]
        self.board.draw_infection_cards()
        self.assertEqual(len(self.board._infection_deck), 0)

    def test_epidemic(self):
        self.board._infection_deck = [MagicMock()]
        self.board.epidemic()
        self.assertEqual(self.board._epidemics_drawn, 1)

if __name__ == '__main__':
    unittest.main()