import gymnasium as gym
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DQN, A2C, PPO
from typing import Callable

from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.logger import configure

from SnakeGame import SnakeGame


def make_env(rank: int, seed: int = 0) -> Callable:

    def _init() -> gym.Env:
        env = SnakeGame(rank)
        env.reset(seed=seed + rank)
        return env

    set_random_seed(seed)
    return _init


def train_multiproc():
    num_cpu = 12  # Number of processes to use
    # Multi-processing
    snakeGame = SubprocVecEnv([make_env(i) for i in range(num_cpu)])
    PPOmodel = PPO("MultiInputPolicy", snakeGame).learn(total_timesteps=900000)

def train_monoproc():
    snakeGame = SnakeGame(0)
    check_env(snakeGame)
    PPOmodel = PPO("MultiInputPolicy", snakeGame).learn(total_timesteps=900000)

def manual():
    snakeGame = SnakeGame(0)
    snakeGame.run()

if __name__ == '__main__':
    train_multiproc()
