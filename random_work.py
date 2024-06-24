import numpy as np
import tensorflow as tf

import gym

from gym.envs.classic_control import CartPoleEnv
import numpy as np

from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.utils import common
from tf_agents.trajectories import trajectory
from tf_agents.replay_buffers import tf_uniform_replay_buffer

replay_buffer: TFUniformReplayBuffer


def main():
    global replay_buffer
    env = CustomCartPole(render_mode='human')

    train_env = tf_py_environment.TFPyEnvironment(env)
    eval_env = tf_py_environment.TFPyEnvironment(env)

    layer_params = (256, 256,)

    agent = create_agent(layer_params,
                         train_env)

    # Replay Buffer
    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
        data_spec=agent.collect_data_spec,
        batch_size=train_env.batch_size,
        max_length=100000
    )

    collect_data(train_env, agent.collect_policy, steps=100)

    dataset-replay_buffer.as_dataset(num_parallel_calls=3,
                                     sample_batch_size=64,
                                     num_steps=2).prefetch(3)

    iterator = iter(dataset)

    # Training loop
    num_iterations = 20000
    for _ in range(num_iterations):
        for _ in range(4):
            collect_data(train_env, agent.collect_policy)

        # Sample a batch of data from the buffer and update the agent's network
        experience, unused_info = next(iterator)
        train_loss = agent.train(experience).loss

        step = agent.train_step_counter.numpy()

        if step % 1000 == 0:
            print(f"Step {step}: Loss = {train_loss:.4f}")

        print(f"Finished training")

    tf_env = tf_py_environment.TFPyEnvironment(eval_env)
    time_step = tf_env.reset()

    reward: float = 1.0
    done: bool = False
    total_reward: float = 0.0
    while not done:
        env.render()
        action_step = agent.policy.action(time_step)
        time_step = tf_env.step(action_step.action)

        observation = time_step.observation.numpy()[0]
        reward = time_step.reward.numpy()[0]

        print(f"Cart position: {observation[0]}")
        print(f"Cart velocity: {observation[1]}")
        print(f"Pole angle: {observation[2]}")
        print(f"Pole angular velocity: {observation[3]}")
        print(f"Reward: {reward}")
        print()
        total_reward += reward
    env.close()

    print(f"Total reward: {total_reward}")


def collect_step(environment, policy):
    global replay_buffer
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(time_step, action_step, next_time_step)
    replay_buffer.add_batch(traj)


def collect_data(env, policy, steps):
    for _ in range(steps):
        collect_step(env, policy)


def create_agent(layers, train_env):
    q_net = q_network.QNetwork(
        train_env.observation_spec(),
        train_env.action_spec(),
        fc_layer_params=layers)

    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-3)
    train_step_counter = tf.Variable(0)

    agent = dqn_agent.DQNAgent(
        train_env.time_step_spec(),
        train_env.action_spec(),
        q_network=q_net,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter)

    agent.initialize()

    return agent


class CustomCartPole(CartPoleEnv):
    def __init__(self, render_mode: str = None):
        super().__init__(render_mode=render_mode)

    def step(self, action):
        # You can modify the step logic here
        observation, reward, done, trunc, info = super().step(action)

        # Modify the reward function
        reward = self.new_reward_calculation(observation, True)

        x_pos = observation[0]
        theta = observation[2]  # Angle of the pole with vertical

        # Determine if the pole has "hit the ground"
        # Let's assume "hitting the ground" is when theta is more than or equal to 12 degrees from vertical
        if abs(theta) <= 1.48 and abs(x_pos) < 2.4:
            done = False
        else:
            done = True
            reward = 0

        return observation, reward, done, trunc, info

    def new_reward_calculation(self, observation, verbose: bool):
        x_position = observation[0]
        deviation = abs(observation[2])

        center_position_reward = 0.417 * max(0, 2.4 - abs(x_position))  # Reward is highest for being at center
        deviation_reward = 4.77 * max(0, 0.2095 - deviation)   # Reward is highest for being straight up


        if verbose:
            print(f"Reward for being in center: {center_position_reward}")
            print(f"Reward for elevation of pole: {deviation}")
        return deviation_reward + center_position_reward # Highest reward is 2

if __name__ == '__main__':
    main()
