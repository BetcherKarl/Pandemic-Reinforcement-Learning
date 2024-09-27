from datetime import date
from time import time
from gymnasium.envs.classic_control import CartPoleEnv
import numpy as np
# import tensorflow as tf
from stable_baselines3 import PPO


class CustomCartPole(CartPoleEnv):
    def __init__(self, render_mode='human'):
        super(CustomCartPole, self).__init__(render_mode=render_mode)

    def step(self, action):
        state, reward, done, trunc, info = super().step(action)

        # Calculate the angle in radians
        x_position = state[0]
        theta = state[2]  # Angle of the pole with vertical

        if (abs(theta) >= 85 * np.pi / 180) or (abs(x_position) >= 2.4):
            done = True
        else:
            done = False

        if done:
            reward = -100  # Penalize the termination with a negative reward
        else:
            reward = self.new_reward(state)

        return state, reward, done, trunc, info

    def new_reward(self, observation):
        cart_position = observation[0]
        # cart_velocity = observation[1]
        theta = observation[2]
        # angular_velocity = observation[3]

        r1 = max(0.0868 * (2.4 - cart_position) ** 2, 0)  # max reward of 0.5
        r2 = max(11.392 * (0.2095 - theta) ** 2, 0)

        return r1 + r2


def main():
    print("Would you like to:\n"
          "\t\"w\": watch a previously trained model\n"
          "\t\"t\": train a new model")

    choice = input("\nEnter an option: ")



    if choice == "w":
        model_name = input("What is the filename of the model you would like to watch? ")
        i = input("How many iterations would you like to watch? ")
        watch_model(model_name, iterations=i)

    elif choice == "t":
        s = int(input("How many steps would you like to train? "))
        train_new_model(steps=s)

    else:
        print("Invalid input")


def train_new_model(steps=10000):
    # Set up the environments the agents will learn in
    env = CustomCartPole()
    model = PPO("MlpPolicy", env, verbose=1)

    print("training...")
    start = time()
    model.learn(total_timesteps=steps)
    print(f"training complete in {time() - start:.2f}s")

    filename = f'CustomCartPole-{date.today()}'
    model.save(f"./models/{filename}")

    watch_model(filename, iterations=5)


def watch_model(filename: str, iterations=10):
    model = PPO.load(f"./models/{filename}")
    vec_env = model.get_env()
    for i in range(iterations):
        total_reward, counter = 0, 0
        obs = vec_env.reset()
        done = False
        while not done:
            vec_env.render()
            action, _states = model.predict(obs)
            observation, reward, done, trunc, info = vec_env.step(action)
            total_reward += reward
            counter += 1
        print(f"Run {i+1}\n"
              f"Total rewards: {total_reward}\n"
              f"Steps survived: {counter}\n"
              f"Average reward / step: {total_reward/counter}\n")
    env.close()


if __name__ == "__main__":
    main()
