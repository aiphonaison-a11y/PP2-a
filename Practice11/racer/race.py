import pygame
import random
import os


class RaceGame:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        def load_image(path, size):
            full_path = os.path.join(self.BASE_DIR, path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Missing image: {full_path}")
            image = pygame.image.load(full_path).convert_alpha()
            return pygame.transform.scale(image, size)

        def load_sound(path):
            full_path = os.path.join(self.BASE_DIR, path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Missing sound: {full_path}")
            return pygame.mixer.Sound(full_path)

        # ---------------- COLORS ----------------
        self.ROAD_GRAY = (70, 70, 70)
        self.LINE_WHITE = (245, 245, 245)
        self.YELLOW = (255, 215, 0)
        self.WHITE = (255, 255, 255)

        # ---------------- FONTS ----------------
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 42)

        # ---------------- OBJECT SIZES ----------------
        self.player_w, self.player_h = 70, 120
        self.enemy_w, self.enemy_h = 70, 120

        # ---------------- IMAGES ----------------
        self.player_img = load_image("images/player_car.png", (self.player_w, self.player_h))
        self.enemy_img = load_image("images/enemy_car.png", (self.enemy_w, self.enemy_h))

        self.yellow_coin_img = load_image("images/coin.png", (30, 30))
        self.blue_coin_img = pygame.transform.rotate(load_image("images/blue_coin.png", (24, 24)), 0)
        self.pink_coin_img = pygame.transform.rotate(load_image("images/pink_coin.png", (22, 22)), 0)

        # ---------------- AUDIO ----------------
        pygame.mixer.music.load(os.path.join(self.BASE_DIR, "sounds/background_music.mp3"))
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

        self.coin_sound = load_sound("sounds/coin_sound.mp3")
        self.crash_sound = load_sound("sounds/crash_sound.mp3")
        self.speed_sound = load_sound("sounds/speed_sound.mp3")

        # ---------------- GAME SETTINGS ----------------
        self.player_speed = 10
        self.coin_speed = 3

        self.enemy_speed_base = 5
        self.enemy_speed = self.enemy_speed_base
        self.speed_increment = 0.15

        self.coin_boost_threshold = 5
        self.last_coin_milestone = 0

        self.game_over = False
        self.reset_game()

    # ---------------- RESET GAME ----------------
    def reset_game(self):
        ex = random.randint(40, self.WIDTH - self.enemy_w - 40)

        self.enemy_x = ex
        self.enemy_y = -150
        self.enemy_speed = self.enemy_speed_base

        self.player_x = self.WIDTH // 2 - self.player_w // 2
        self.player_y = self.HEIGHT - 150

        enemy_rect = pygame.Rect(ex, self.enemy_y, self.enemy_w, self.enemy_h)
        self.coin_x, self.coin_y = self.spawn_coin(enemy_rect)

        self.score = 0
        self.coins = 0
        self.game_over = False
        self.last_coin_milestone = 0

    # ---------------- RANDOM COIN TYPE ----------------
    def choose_coin_type(self):
        chance = random.randint(1, 100)

        if chance <= 8:
            return self.pink_coin_img, 10
        elif chance <= 28:
            return self.blue_coin_img, 5
        else:
            return self.yellow_coin_img, 1

    # ---------------- SPAWN COIN ----------------
    def spawn_coin(self, enemy_rect):
        self.coin_img, self.coin_value = self.choose_coin_type()

        self.current_coin_w = self.coin_img.get_width()
        self.current_coin_h = self.coin_img.get_height()

        while True:
            x = random.randint(40, self.WIDTH - self.current_coin_w - 40)
            y = random.randint(-400, -100)

            coin_rect = pygame.Rect(x, y, self.current_coin_w, self.current_coin_h)

            if not coin_rect.colliderect(enemy_rect):
                return x, y

    # ---------------- PLAYER MOVEMENT ----------------
    def handle_input(self, keys):
        if keys[pygame.K_LEFT] and self.player_x > 5:
            self.player_x -= self.player_speed

        if keys[pygame.K_RIGHT] and self.player_x < self.WIDTH - self.player_w - 5:
            self.player_x += self.player_speed

    # ---------------- UPDATE GAME ----------------
    def update(self):
        if self.game_over:
            return

        self.enemy_y += self.enemy_speed

        if self.enemy_y > self.HEIGHT:
            self.enemy_y = -150
            self.enemy_x = random.randint(40, self.WIDTH - self.enemy_w - 40)

            self.score += 1
            self.enemy_speed += self.speed_increment

        enemy_rect = pygame.Rect(self.enemy_x, self.enemy_y, self.enemy_w, self.enemy_h)

        self.coin_y += self.coin_speed

        if self.coin_y > self.HEIGHT:
            self.coin_x, self.coin_y = self.spawn_coin(enemy_rect)

        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_w, self.player_h)
        coin_rect = pygame.Rect(self.coin_x, self.coin_y, self.current_coin_w, self.current_coin_h)

        # enemy collision
        if player_rect.colliderect(enemy_rect):
            self.crash_sound.play()
            self.game_over = True

        # coin collision
        if player_rect.colliderect(coin_rect):
            self.coins += self.coin_value
            self.coin_sound.play()
            self.coin_x, self.coin_y = self.spawn_coin(enemy_rect)

        # enemy speed increase every 5 coins
        if self.coins >= self.coin_boost_threshold and self.coins % self.coin_boost_threshold == 0:
            if self.coins != self.last_coin_milestone:
                self.enemy_speed += 0.35
                self.speed_sound.play()
                self.last_coin_milestone = self.coins

    # ---------------- DRAW SCREEN ----------------
    def draw(self):
        self.screen.fill(self.ROAD_GRAY)

        pygame.draw.line(self.screen, self.LINE_WHITE, (120, 0), (120, self.HEIGHT), 4)
        pygame.draw.line(self.screen, self.LINE_WHITE, (240, 0), (240, self.HEIGHT), 4)

        self.screen.blit(self.player_img, (self.player_x, self.player_y))
        self.screen.blit(self.enemy_img, (self.enemy_x, self.enemy_y))
        self.screen.blit(self.coin_img, (self.coin_x, self.coin_y))

        self.screen.blit(self.font.render(f"Avoided: {self.score}", True, self.YELLOW), (10, 10))
        self.screen.blit(self.font.render(f"Coins: {self.coins}", True, self.YELLOW), (10, 40))

        if self.game_over:
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.set_alpha(140)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            self.screen.blit(self.big_font.render("GAME OVER", True, self.YELLOW), (75, 180))
            self.screen.blit(self.font.render(f"Score: {self.score}", True, self.WHITE), (120, 260))
            self.screen.blit(self.font.render(f"Coins: {self.coins}", True, self.WHITE), (120, 300))
            self.screen.blit(self.font.render("R - Restart   Q - Quit", True, self.WHITE), (75, 360))

    # ---------------- GAME EVENTS ----------------
    def handle_events(self, event):
        if self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_q:
                return False
        return True