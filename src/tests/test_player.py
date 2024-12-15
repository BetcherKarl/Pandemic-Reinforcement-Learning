import unittest
from unittest.mock import MagicMock
from player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.board = MagicMock()
        self.board.cities = {'Atlanta': MagicMock()}
        self.player = Player(board=self.board, starting_city='Atlanta')

    def test_hand_getter(self):
        self.assertEqual(self.player.hand, [])

    def test_hand_setter(self):
        new_hand = ['card1', 'card2']
        self.player.hand = new_hand
        self.assertEqual(self.player.hand, new_hand)

    def test_add_to_hand(self):
        card = 'card1'
        self.player.add_to_hand(card)
        self.assertIn(card, self.player.hand)

if __name__ == '__main__':
    unittest.main()