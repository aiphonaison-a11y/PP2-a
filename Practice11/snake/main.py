import pygame
import random
import sys
from snake import Snake, UP, DOWN, LEFT, RIGHT

pygame.init()

WIDTH, HEIGHT = 400, 400
CELL = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake 2.0")
clock = pygame.time.Clock()

# Colors
RED = (255, 0, 0)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 0)
VIOLET = (148, 0, 211)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 48)


def random_pos(snake_body, forbidden=[]):
    while True:
        pos = (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )
        if pos not in snake_body and pos not in forbidden:
            return pos


# -------- RANDOM FOOD GENERATOR --------
def generate_food(snake_body, poison):
    chance = random.randint(1, 100)

    if chance <= 15:
        color = GREEN
        value = 5
        timer = 150   # 15 seconds
    elif chance <= 40:
        color = YELLOW
        value = 3
        timer = None
    else:
        color = RED
        value = 1
        timer = None

    pos = random_pos(snake_body, [poison] if poison else [])
    return pos, color, value, timer


def game_over_screen(score):
    while True:
        screen.fill(BLACK)

        text1 = big_font.render("GAME OVER", True, RED)
        text2 = font.render(f"Score: {score}", True, WHITE)
        text3 = font.render("Press R to Restart or Q to Quit", True, GRAY)

        screen.blit(text1, (80, 140))
        screen.blit(text2, (150, 200))
        screen.blit(text3, (40, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    snake = Snake()

    poison = None
    poison_timer = 0
    POISON_DURATION = 80
    POISON_CHANCE = 0.02

    food, food_color, food_value, green_timer = generate_food(snake.snake, poison)

    score = 0
    SPEED = 10

    while True:
        clock.tick(SPEED)

        # -------- INPUT --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        # -------- POISON SPAWN --------
        if poison is None:
            if random.random() < POISON_CHANCE:
                poison = random_pos(snake.snake, [food])
                poison_timer = POISON_DURATION
        else:
            poison_timer -= 1
            if poison_timer <= 0:
                poison = None

        # -------- GREEN FOOD TIMER --------
        if food_color == GREEN and green_timer is not None:
            green_timer -= 1
            if green_timer <= 0:
                food, food_color, food_value, green_timer = generate_food(snake.snake, poison)

        head = snake.snake[-1]

        grow = False
        shrink = False

        # -------- FOOD / POISON CHECK --------
        if head == food:
            grow = True
            score += food_value
            food, food_color, food_value, green_timer = generate_food(snake.snake, poison)

        elif poison is not None and head == poison:
            shrink = True
            score = max(0, score - 1)
            poison = None

        alive = snake.move(grow=grow, shrink=shrink)

        if not alive:
            game_over_screen(score)
            return

        # -------- DRAW --------
        screen.fill(BLACK)

        pygame.draw.rect(screen, food_color, (*food, CELL, CELL))

        if poison is not None:
            pygame.draw.rect(screen, VIOLET, (*poison, CELL, CELL))

        for part in snake.snake[:-1]:
            screen.blit(snake.skin, part)
        screen.blit(snake.head, snake.snake[-1])

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if food_color == GREEN and green_timer is not None:
            seconds = green_timer // SPEED
            timer_text = small_font.render(f"Green bonus: {seconds}s", True, GREEN)
            screen.blit(timer_text, (220, 10))

        pygame.display.update()


while True:
    main()