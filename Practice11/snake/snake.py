import pygame

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

CELL = 10
WIDTH = 600
HEIGHT = 600


class Snake:
    def __init__(self):
        self.snake = [(300, 300), (310, 300), (320, 300)]
        self.direction = RIGHT

        self.skin = pygame.Surface((CELL, CELL))
        self.skin.fill((255, 255, 255))

        self.head = pygame.Surface((CELL, CELL))
        self.head.fill((200, 200, 200))

    def move(self, grow=False, shrink=False):
        head_x, head_y = self.snake[-1]

        if self.direction == RIGHT:
            new_head = (head_x + CELL, head_y)
        elif self.direction == LEFT:
            new_head = (head_x - CELL, head_y)
        elif self.direction == UP:
            new_head = (head_x, head_y - CELL)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + CELL)

        # wall collision
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            return False

        # self collision
        if new_head in self.snake:
            return False

        self.snake.append(new_head)

        if not grow:
            self.snake.pop(0)

        # poison shrink one extra block
        if shrink and len(self.snake) > 1:
            self.snake.pop(0)

        return True