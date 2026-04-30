import pygame
from config import *

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Snake:
    def __init__(self, color):
        self.snake = [(300, 300), (310, 300), (320, 300)]
        self.direction = RIGHT
        self.color = color
        self.shield = False

    def draw(self, screen):
        # body
        for part in self.snake[:-1]:
            pygame.draw.rect(screen, self.color, (*part, CELL, CELL))

        # head
        pygame.draw.rect(screen, GRAY, (*self.snake[-1], CELL, CELL))

    def move(self, grow=False, shrink=False, obstacles=[]):
        x, y = self.snake[-1]

        if self.direction == RIGHT:
            new_head = (x + CELL, y)
        elif self.direction == LEFT:
            new_head = (x - CELL, y)
        elif self.direction == UP:
            new_head = (x, y - CELL)
        else:
            new_head = (x, y + CELL)

        collision = False

        # border collision
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            collision = True

        # self collision
        if new_head in self.snake:
            collision = True

        # obstacle collision
        if new_head in obstacles:
            collision = True

        # shield saves once
        if collision:
            if self.shield:
                self.shield = False
                return True
            return False

        self.snake.append(new_head)

        if not grow:
            self.snake.pop(0)

        # poison shrink by 2
        if shrink:
            if len(self.snake) <= 2:
                return False
            self.snake.pop(0)
            self.snake.pop(0)

        return True