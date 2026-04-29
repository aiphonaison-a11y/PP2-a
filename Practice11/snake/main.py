import pygame
import random
import sys
from snake import Snake, UP, DOWN, LEFT, RIGHT

pygame.init()

WIDTH, HEIGHT = 600, 600
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

DARK1 = (40, 40, 40)
DARK2 = (55, 55, 55)
CYAN = (0, 255, 255)

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 42)


# ---------------- CHESS BOARD ----------------
def draw_board():
    for y in range(0, HEIGHT, CELL):
        for x in range(0, WIDTH, CELL):
            color = DARK1 if (x // CELL + y // CELL) % 2 == 0 else DARK2
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))


# ---------------- POSITION ----------------
def random_pos(snake_body, forbidden=[]):
    while True:
        pos = (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )
        if pos not in snake_body and pos not in forbidden:
            return pos


# ---------------- INSTRUCTIONS ----------------
def show_instructions():
    while True:
        screen.fill(BLACK)

        screen.blit(big_font.render("SNAKE GAME", True, WHITE), (210, 60))

        lines = [
            "CONTROLS:",
            "Arrow Keys - Move",
            "",
            "FOOD:",
            "Red = +1",
            "Yellow = +3",
            "Green = +5 (15 sec timer)",
            "",
            "POISON:",
            "Purple = -3 points + shrink",
            "",
            "LEVEL SYSTEM:",
            "Level up every 15 points",
            "Each level adds +5 speed",
            "",
            "Press SPACE to start"
        ]

        y = 140
        for line in lines:
            color = WHITE

            if "Red" in line:
                color = RED
            elif "Yellow" in line:
                color = YELLOW
            elif "Green" in line:
                color = GREEN
            elif "Purple" in line:
                color = VIOLET
            elif "LEVEL SYSTEM" in line:
                color = CYAN

            text = small_font.render(line, True, color)
            screen.blit(text, (160, y))
            y += 26

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


# ---------------- FOOD ----------------
def generate_food(snake_body, poison):
    chance = random.randint(1, 100)

    if chance <= 15:
        return random_pos(snake_body, [poison] if poison else []), GREEN, 5, 150
    elif chance <= 40:
        return random_pos(snake_body, [poison] if poison else []), YELLOW, 3, None
    else:
        return random_pos(snake_body, [poison] if poison else []), RED, 1, None


# ---------------- GAME OVER ----------------
def game_over_screen(score, level):
    while True:
        screen.fill(BLACK)

        screen.blit(big_font.render("GAME OVER", True, RED), (200, 220))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (250, 280))
        screen.blit(font.render(f"Level: {level}", True, CYAN), (250, 310))
        screen.blit(font.render("R - Restart | Q - Quit", True, WHITE), (190, 360))

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


# ---------------- MAIN GAME ----------------
def main():
    show_instructions()

    snake = Snake()

    poison = None
    poison_timer = 0
    POISON_DURATION = 80
    POISON_CHANCE = 0.02

    food, food_color, food_value, green_timer = generate_food(snake.snake, poison)

    score = 0
    base_speed = 10
    SPEED = 10
    level = 1

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

        # -------- POISON --------
        if poison is None:
            if random.random() < POISON_CHANCE:
                poison = random_pos(snake.snake, [food])
                poison_timer = POISON_DURATION
        else:
            poison_timer -= 1
            if poison_timer <= 0:
                poison = None

        # -------- GREEN TIMER --------
        if food_color == GREEN and green_timer is not None:
            green_timer -= 1
            if green_timer <= 0:
                food, food_color, food_value, green_timer = generate_food(snake.snake, poison)

        head = snake.snake[-1]

        grow = False
        shrink = False

        # -------- FOOD --------
        if head == food:
            grow = True
            score += food_value
            food, food_color, food_value, green_timer = generate_food(snake.snake, poison)

        # -------- POISON --------
        elif poison is not None and head == poison:
            shrink = True
            score = max(0, score - 3)
            poison = None

        # -------- LEVEL SYSTEM --------
        level = (score // 15) + 1
        if level > 4:
            level = 4

        SPEED = base_speed + (level - 1) * 5

        # -------- MOVE --------
        alive = snake.move(grow=grow, shrink=shrink)

        if not alive:
            game_over_screen(score, level)
            return

        # -------- DRAW --------
        draw_board()

        pygame.draw.rect(screen, food_color, (*food, CELL, CELL))

        if poison is not None:
            pygame.draw.rect(screen, VIOLET, (*poison, CELL, CELL))

        for part in snake.snake[:-1]:
            screen.blit(snake.skin, part)
        screen.blit(snake.head, snake.snake[-1])

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, CYAN), (10, 40))

        if food_color == GREEN and green_timer is not None:
            screen.blit(
                small_font.render(f"Green: {green_timer // 10}s", True, GREEN),
                (430, 10)
            )

        pygame.display.update()


while True:
    main()