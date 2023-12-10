import random

import gymnasium as gym
import sys
import numpy as np
import math
import pygame
from gymnasium import spaces
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import A2C

from Snake import Snake

SCREEN_SIZE = (720, 720)
GRID_SIZE = 30
DEFAULT_COORD = [0, 0]
DEFAULT_DIR = "right"
SPEED = 5  # FPS


def generate_new_apple():
    x = random.randint(0, int(SCREEN_SIZE[0] / GRID_SIZE) - 1)
    y = random.randint(0, int(SCREEN_SIZE[1] / GRID_SIZE) - 1)
    return [x, y]


class SnakeGame(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.snake = Snake(DEFAULT_COORD, DEFAULT_DIR)
        self.apple = generate_new_apple()

    def step(self, action):
        self.snake.dir = action
        self.snake.step()

        self.check_border_collisions()
        self.check_apple_collisions()

        self.render()

    def reset(self, **kwargs):
        self.snake = Snake(DEFAULT_COORD, DEFAULT_DIR)
        self.apple = generate_new_apple()

    def close(self):
        sys.exit(0)

    def render(self):
        self.screen.fill("black")
        self.draw_apple()
        self.draw_snake()

        # Update screen
        pygame.display.flip()
        self.clock.tick(SPEED)

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

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return "up"
        if keys[pygame.K_DOWN]:
            return "down"
        if keys[pygame.K_RIGHT]:
            return "right"
        if keys[pygame.K_LEFT]:
            return "left"
        return self.snake.dir

    def check_border_collisions(self):
        if (self.snake.head[0] < 0
                or self.snake.head[0] >= int(SCREEN_SIZE[0] / GRID_SIZE)
                or self.snake.head[1] < 0
                or self.snake.head[1] >= int(SCREEN_SIZE[1] / GRID_SIZE)):
            self.reset()

    def check_apple_collisions(self):
        if self.snake.head == self.apple:
            self.snake.eat()
            self.apple = generate_new_apple()

    def run(self):
        while self.running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.step(self.get_input())
