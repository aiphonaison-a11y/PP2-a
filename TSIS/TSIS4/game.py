import pygame
import random
import sys
import json
import os

from config import *
from snake import Snake, UP, DOWN, LEFT, RIGHT
from db import save_result, get_top10, get_best

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 Snake Final")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)
big_font = pygame.font.SysFont("Arial", 42)


# ---------------- SETTINGS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")


def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings_file(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)


settings = load_settings()


# ---------------- DRAW BOARD ----------------
def draw_board():
    if settings["grid"]:
        for y in range(0, HEIGHT, CELL):
            for x in range(0, WIDTH, CELL):
                color = DARK1 if (x // CELL + y // CELL) % 2 == 0 else DARK2
                pygame.draw.rect(screen, color, (x, y, CELL, CELL))
    else:
        screen.fill(BLACK)


# ---------------- RANDOM POSITION ----------------
def random_pos(snake_body, forbidden=[]):
    while True:
        pos = (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )
        if pos not in snake_body and pos not in forbidden:
            return pos


# ---------------- FOOD ----------------
def generate_food(snake_body, poison, obstacles, powerup):
    chance = random.randint(1, 100)
    forbidden = obstacles[:]
    if poison:
        forbidden.append(poison)
    if powerup:
        forbidden.append(powerup[0])

    if chance <= 15:
        return random_pos(snake_body, forbidden), GREEN, 5, 150
    elif chance <= 40:
        return random_pos(snake_body, forbidden), YELLOW, 3, None
    else:
        return random_pos(snake_body, forbidden), RED, 1, None


# ---------------- OBSTACLES ----------------
def generate_obstacles(level, snake_body):
    obstacles = []
    if level >= 3:
        count = level * 6
        while len(obstacles) < count:
            pos = random_pos(snake_body, obstacles)
            if abs(pos[0] - snake_body[-1][0]) > 50 or abs(pos[1] - snake_body[-1][1]) > 50:
                obstacles.append(pos)
    return obstacles


# ---------------- POWERUP ----------------
def spawn_powerup(snake_body, food, poison, obstacles):
    types = ["speed", "slow", "shield"]
    t = random.choice(types)
    forbidden = obstacles[:]
    forbidden.append(food)
    if poison:
        forbidden.append(poison)
    return (random_pos(snake_body, forbidden), t, pygame.time.get_ticks())


# ---------------- USERNAME INPUT ----------------
def username_screen():
    username = ""
    while True:
        screen.fill(BLACK)
        screen.blit(big_font.render("ENTER USERNAME", True, CYAN), (150, 200))
        screen.blit(font.render(username, True, WHITE), (240, 270))
        screen.blit(small_font.render("Press ENTER to continue", True, WHITE), (200, 330))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username != "":
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 12:
                        username += event.unicode


# ---------------- LEADERBOARD SCREEN ----------------
def leaderboard_screen():
    data = get_top10()

    while True:
        screen.fill(BLACK)
        screen.blit(big_font.render("TOP 10 LEADERBOARD", True, CYAN), (120, 40))

        y = 100
        for i, row in enumerate(data):
            txt = f"{i+1}. {row[0]} | Score:{row[1]} | Level:{row[2]} | {row[3].strftime('%m-%d')}"
            screen.blit(small_font.render(txt, True, WHITE), (60, y))
            y += 35

        screen.blit(font.render("Press B to go back", True, WHITE), (200, 540))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# ---------------- SETTINGS SCREEN ----------------
def settings_screen():
    global settings
    colors = [
        [255,255,255],
        [0,255,255],
        [255,0,255],
        [0,255,0]
    ]
    idx = 0

    while True:
        screen.fill(BLACK)
        screen.blit(big_font.render("SETTINGS", True, CYAN), (220, 100))
        screen.blit(font.render(f"G - Grid: {settings['grid']}", True, WHITE), (180, 220))
        screen.blit(font.render(f"S - Sound: {settings['sound']}", True, WHITE), (180, 260))
        screen.blit(font.render("C - Change Snake Color", True, WHITE), (180, 300))
        screen.blit(font.render("B - Save & Back", True, WHITE), (180, 340))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]
                elif event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]
                elif event.key == pygame.K_c:
                    idx = (idx + 1) % len(colors)
                    settings["snake_color"] = colors[idx]
                elif event.key == pygame.K_b:
                    save_settings_file(settings)
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# ---------------- MAIN MENU ----------------
def main_menu():
    while True:
        screen.fill(BLACK)
        screen.blit(big_font.render("TSIS 4 SNAKE", True, CYAN), (180, 120))
        screen.blit(font.render("1 - Play", True, WHITE), (240, 230))
        screen.blit(font.render("2 - Leaderboard", True, WHITE), (240, 270))
        screen.blit(font.render("3 - Settings", True, WHITE), (240, 310))
        screen.blit(font.render("4 - Quit", True, WHITE), (240, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    leaderboard_screen()
                elif event.key == pygame.K_3:
                    settings_screen()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# ---------------- GAME OVER ----------------
def game_over(score, level, best):
    while True:
        screen.fill(BLACK)
        screen.blit(big_font.render("GAME OVER", True, RED), (200, 200))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (220, 270))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (220, 300))
        screen.blit(font.render(f"Personal Best: {best}", True, CYAN), (180, 330))
        screen.blit(font.render("R - Retry | M - Menu", True, WHITE), (170, 390))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                elif event.key == pygame.K_m:
                    return "menu"
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# ---------------- MAIN GAME LOOP ----------------
def play_game():
    username = username_screen()
    personal_best = get_best(username)

    snake = Snake(tuple(settings["snake_color"]))
    poison = None
    poison_timer = 0

    powerup = None
    powerup_spawn_timer = pygame.time.get_ticks()
    active_effect = None
    effect_end = 0

    score = 0
    level = 1
    speed = BASE_SPEED
    obstacles = []

    food, food_color, food_value, green_timer = generate_food(snake.snake, poison, obstacles, None)

    while True:
        if active_effect == "speed" and pygame.time.get_ticks() > effect_end:
            speed = BASE_SPEED + (level - 1) * 5
            active_effect = None

        if active_effect == "slow" and pygame.time.get_ticks() > effect_end:
            speed = BASE_SPEED + (level - 1) * 5
            active_effect = None

        clock.tick(speed)

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

        if poison is None and random.random() < 0.02:
            poison = random_pos(snake.snake, [food] + obstacles)
            poison_timer = 80
        elif poison:
            poison_timer -= 1
            if poison_timer <= 0:
                poison = None

        if powerup is None and pygame.time.get_ticks() - powerup_spawn_timer > 10000:
            powerup = spawn_powerup(snake.snake, food, poison, obstacles)

        if powerup and pygame.time.get_ticks() - powerup[2] > 8000:
            powerup = None
            powerup_spawn_timer = pygame.time.get_ticks()

        if food_color == GREEN and green_timer:
            green_timer -= 1
            if green_timer <= 0:
                food, food_color, food_value, green_timer = generate_food(snake.snake, poison, obstacles, powerup)

        head = snake.snake[-1]
        grow = False
        shrink = False

        if head == food:
            grow = True
            score += food_value
            food, food_color, food_value, green_timer = generate_food(snake.snake, poison, obstacles, powerup)

        elif poison and head == poison:
            shrink = True
            score = max(0, score - 3)
            poison = None

        elif powerup and head == powerup[0]:
            if powerup[1] == "speed":
                speed += 8
                active_effect = "speed"
                effect_end = pygame.time.get_ticks() + 5000
            elif powerup[1] == "slow":
                speed = max(5, speed - 5)
                active_effect = "slow"
                effect_end = pygame.time.get_ticks() + 5000
            elif powerup[1] == "shield":
                snake.shield = True

            powerup = None
            powerup_spawn_timer = pygame.time.get_ticks()

        level = min((score // 15) + 1, 5)
        speed = BASE_SPEED + (level - 1) * 5 if active_effect is None else speed
        obstacles = generate_obstacles(level, snake.snake)

        alive = snake.move(grow=grow, shrink=shrink, obstacles=obstacles)

        if not alive:
            save_result(username, score, level)
            action = game_over(score, level, max(personal_best, score))
            if action == "retry":
                return play_game()
            else:
                return

        draw_board()

        for ob in obstacles:
            pygame.draw.rect(screen, BLUE, (*ob, CELL, CELL))

        pygame.draw.rect(screen, food_color, (*food, CELL, CELL))

        if poison:
            pygame.draw.rect(screen, VIOLET, (*poison, CELL, CELL))

        if powerup:
            color = CYAN if powerup[1] == "speed" else YELLOW if powerup[1] == "slow" else WHITE
            pygame.draw.rect(screen, color, (*powerup[0], CELL, CELL))

        snake.draw(screen)

        screen.blit(font.render(f"Score:{score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level:{level}", True, CYAN), (10, 35))
        screen.blit(font.render(f"Best:{personal_best}", True, GREEN), (10, 60))
        if snake.shield:
            screen.blit(font.render("Shield ON", True, YELLOW), (470, 10))

        pygame.display.update()