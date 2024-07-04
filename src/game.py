from utils.board import PandemicBoard
from utils.card import Card
from constants import board_size, r_seed

import numpy as np
import pygame as pg

import json
from threading import Thread
from time import sleep
import random
from typing import Tuple

board: PandemicBoard
board = PandemicBoard(num_players=4, seed=r_seed)

# function to test behavior of code
def wait_test(wait_time=2):
    global board
    print("Running a small test case")
    board._colors["red"].cured = True
    board.cities["Bangkok"]._disease_cubes = {'blue': 0, 'yellow': 0, 'black': 0, 'red': 0}
    # board._colors["red"].eradicate()
    for i in range(8):
        sleep(wait_time)
        board.current_player.save_the_day(wait_time=wait_time/2)
        sleep(wait_time / 2)
        board.next_player()


testing_thread = Thread(target=wait_test)
testing_thread.start()
# str4tttttttttttttttttttttttttttttttttttett5t - Merlin (my cat)

for player in board.players:
    print(f"Player {player.role}")
    for card in player.hand:
        print(f"{card.color} ({card.name})")
    print()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # TODO: Click to view cards in discards
    board.render()

    if len(board._player_deck) == 58 - len(board.players) * (6 - len(board.players)) - 16: # what the fuck is this
        print("Test case finished successfully")
        break

print("Game Over")