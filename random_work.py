import numpy as np
import tensorflow as tf

import gym
from gym.envs.classic_control import CartPoleEnv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class CustomCartPole(CartPoleEnv):
    def __init__(self, render_mode: str = None):
        super().__init__(render_mode=render_mode)

    def step(self, action):
        # You can modify the step logic here
        observation, reward, done, trunc, info = super().step(action)

        # Modify the reward function
        reward = new_reward_calculation(observation, True)

        x_pos = observation[0]
        theta = observation[2]  # Angle of the pole with vertical

        # Determine if the pole has "hit the ground" or the cart has left the screen
        # Let's assume "hitting the ground" is when theta is more than or equal to 85 degrees from vertical
        if abs(theta) <= 1.48 and abs(x_pos) < 2.4:
            done = False
        else:
            done = True
            reward = 0

        return observation, reward, done, trunc, info


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)


if __name__ == '__main__':
    main()
