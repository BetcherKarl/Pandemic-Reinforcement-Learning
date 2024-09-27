"""A tf_agents environment for learning the game of Pandemic"""

import gym
import pygame as pg

from .board import PandemicBoard


class PandemicEnvironment(gym.Env):
    def __init__(self, num_players=4):
        self.board = PandemicBoard(num_players=num_players)

    def step(self, action):
        raise NotImplementedError('PandemicEnvironment.step not implemented')

    def render(self, mode='human'):
        if mode == 'rgb_array':
            logger.warn('rgb_array is not implemented. sucks to suck.')
        board.draw()

    def reset(self):
        players = len(self.board.players)
        self.board = PandemicBoard(num_players=players)

    def close(self):
        raise NotImplementedError('PandemicEnvironment.close not implemented')

    @property
    def board(self) -> PandemicBoard:
        return board

    @board.setter
    def board(self, other: PandemicBoard):
        self.board = other
