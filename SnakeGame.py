import math
import random
import os

import gymnasium as gym
import sys

import numpy as np
import pygame
from gymnasium import spaces

from Snake import Snake

SCREEN_SIZE = (720 / 2, 720 / 2)
GRID_SIZE = 30

N_CELLS = int(SCREEN_SIZE[0] / GRID_SIZE)


DEFAULT_COORD = [0, 0]
DEFAULT_DIR = 2
SPEED = 5  # FPS


def generate_new_apple():
    x = random.randint(0, N_CELLS - 1)
    y = random.randint(0, N_CELLS - 1)
    return [x, y]


class SnakeGame(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, rank):
        super().__init__()

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Dict({"apple": spaces.Box(low=0, high=int(SCREEN_SIZE[0] / GRID_SIZE), shape=(2,), dtype=np.int32),
                                              "snake_body": spaces.Box(low=-1, high=N_CELLS, shape=(N_CELLS*N_CELLS,), dtype=np.int32),
                                              "snake_head": spaces.Box(low=-1, high=int(SCREEN_SIZE[0] / GRID_SIZE), shape=(2,), dtype=np.int32),
                                              "snake_dir": spaces.Discrete(4)
                                              })

        # pygame setup
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_SIZE[0]*(rank % 3), SCREEN_SIZE[1]*(rank // 3))
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        self.running = True

        self.snake = Snake(DEFAULT_COORD, DEFAULT_DIR)
        self.apple = generate_new_apple()
        self.step_count = 0
        self.best_reward = 0

    def step(self, action):
        self.step_count += 1

        self.snake.step(action)

        terminated = self.check_border_collisions() or self.check_snake_collisions()
        observation = self.get_observation()
        reward = math.exp(len(self.snake.body))  # * 1/math.pow(self.step_count, 0.1)

        self.check_apple_collisions()

        if reward > self.best_reward:
            self.best_reward = reward
            print("New Best Reward = " + str(reward))

        self.render()

        return observation, reward, terminated, False, {}

    def reset(self, **kwargs):
        self.snake = Snake(DEFAULT_COORD, DEFAULT_DIR)
        self.apple = generate_new_apple()
        self.step_count = 0

        observation = self.get_observation()

        return observation, {}

    def close(self):
        pygame.quit()
        pass

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.screen.fill("black")
        self.draw_apple()
        self.draw_snake()

        # Update screen
        pygame.display.flip()
        # self.clock.tick(SPEED)

    def draw_snake(self):
        # Draw Head
        head = pygame.Rect(self.snake.head[0] * GRID_SIZE, self.snake.head[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, "green", head)

        # Draw Body
        for bodyPart in self.snake.body:
            rect = pygame.Rect(bodyPart[0] * GRID_SIZE, bodyPart[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, "green", rect)

    def draw_apple(self):
        # Draw Head
        head = pygame.Rect(self.apple[0] * GRID_SIZE, self.apple[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, "red", head)

    def check_border_collisions(self):
        if (self.snake.head[0] < 0
                or self.snake.head[0] >= int(SCREEN_SIZE[0] / GRID_SIZE)
                or self.snake.head[1] < 0
                or self.snake.head[1] >= int(SCREEN_SIZE[1] / GRID_SIZE)):
            return True
        return False

    def check_apple_collisions(self):
        if self.snake.head == self.apple:
            self.snake.eat()
            self.apple = generate_new_apple()

    def check_snake_collisions(self):
        for bodyPart in self.snake.body:
            if self.snake.head == bodyPart:
                return True
        return False

    def get_observation(self):
        snake_body = np.zeros(shape=(N_CELLS * N_CELLS,), dtype=np.int32)
        snake_body = snake_body - 1

        for bodyPart, index in enumerate(self.snake.body):
            snake_body[index] = bodyPart

        return {
            "apple": np.array(self.apple, dtype=np.int32),
            "snake_body": snake_body,
            "snake_head": np.array(self.snake.head, dtype=np.int32),
            "snake_dir": self.snake.dir
        }

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            return 1
        if keys[pygame.K_LEFT]:
            return 0
        return 2

    def run(self):
        while self.running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            data = self.step(self.get_input())
            if data[2]:
                self.reset()
