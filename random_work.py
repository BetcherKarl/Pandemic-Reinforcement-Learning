# import gym
# from gym.envs.classic_control import CartPoleEnv
# import numpy as np
# import tensorflow as tf
# from tf_agents.environments import suite_gym
# from tf_agents.environments import tf_py_environment
# from tf_agents.networks import q_network
# from tf_agents.agents.dqn import dqn_agent
# from tf_agents.utils import common
# from tf_agents.trajectories import trajectory
# from tf_agents.replay_buffers import tf_uniform_replay_buffer
#
#
# class CustomCartPole(CartPoleEnv):
#     def __init__(self, render_mode='human'):
#         super(CustomCartPole, self).__init__(render_mode=render_mode)
#
#     def step(self, action):
#         state, reward, done, trunc, info = super().step(action)
#
#         # Calculate the angle in radians
#         x_position = state[0]
#         theta = state[2]  # Angle of the pole with vertical
#
#         if (abs(theta) >= 85 * np.pi / 180) or (abs(x_position) >= 2.4):
#             done = True
#         else:
#             done = False
#
#         if done:
#             reward = -100  # Penalize the termination with a negative reward
#         else:
#             reward = self.new_reward(state)
#
#         return state, reward, done, trunc, info
#
#     def new_reward(self, observation):
#         cart_position = observation[0]
#         # cart_velocity = observation[1]
#         theta = observation[2]
#         # angular_velocity = observation[3]
#
#         r1 = max(0.0868 * (2.4 - cart_position) ** 2, 0)  # max reward of 0.5
#         r2 = max(11.392 * (0.2095 - theta) ** 2, 0)
#
#         return r1 + r2
#
#
# def main():
#     # Set up the environments the agents will learn in
#     env = CustomCartPole()
#     train_env = tf_py_environment.TFPyEnvironment(env)
#     train_env = tf_py_environment.TFPyEnvironment(env)
#
#     # Define the q-network
#     fc_layer_params = (100,)
#     q_net = q_network.QNetwork(
#         train_env.observation_spec(),
#         train_env.action_spec(),
#         fc_layer_params=fc_layer_params)
#
#     # Define the DQN Agent
#     optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-3)
#     train_step_counter = tf.Variable(0)
#
#     agent = dqn_agent.DqnAgent(
#         train_env.time_step_spec(),
#         train_env.action_spec(),
#         q_network=q_net,
#         optimizer=optimizer,
#         td_errors_loss_fn=common.element_wise_squared_loss,
#         train_step_counter=train_step_counter)
#
#     agent.initialize()
#
#     # Replay Buffer
#     replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
#         data_spec=agent.collect_data_spec,
#         batch_size=train_env.batch_size,
#         max_length=100000)
#
#     # Data Collection
#     collect_data(train_env, agent.collect_policy, steps=100)
#
#     # Sample a batch of data from the buffer and train the agent
#     dataset = replay_buffer.as_dataset(
#         num_parallel_calls=3,
#         sample_batch_size=64,
#         num_steps=2).prefetch(3)
#
#     iterator = iter(dataset)
#
#     # Training the agent
#     num_iterations = 20000
#
#     for _ in range(num_iterations):
#         # Collect a few steps using collect_policy and save to the replay buffer.
#         for _ in range(4):
#             collect_step(train_env, agent.collect_policy)
#
#         # Sample a batch of data from the buffer and update the agent's network.
#         experience, unused_info = next(iterator)
#         train_loss = agent.train(experience).loss
#
#         step = agent.train_step_counter.numpy()
#
#         if step % 1000 == 0:
#             print('step = {0}: loss = {1}'.format(step, train_loss))
#
#     # You might want to evaluate the agent's performance here
#     print("Finished training!")
#
#
# def old_main():
#     env = CustomCartPole()
#
#     observation = env.reset()
#     done = False
#     while not done:
#         env.render()
#         action = env.action_space.sample()  # replace this with your agent's action
#         print('test 4')
#         observation, reward, done, trunc, info = env.step(action)
#         if bool(done):
#             observation = env.reset()
#     env.close()
#
#
# def collect_data(env, policy, steps):
#     for _ in range(steps):
#         collect_step(env, policy)
#
#
# def collect_step(environment, policy):
#     time_step = environment.current_time_step()
#     action_step = policy.action(time_step)
#     next_time_step = environment.step(action_step.action)
#     traj = trajectory.from_transition(time_step, action_step, next_time_step)
#     replay_buffer.add_batch(traj)

import json
import os
def temp_main():
    path = "modlist.json"
    with open('modlist.json', 'r') as f:
        mods = sorted(json.load(f), key=lambda x: x["archiveName"])
    mod_names = []
    for mod in mods:
        mod_names.append()



if __name__ == '__main__':
    temp_main()
