import pygame
import random
import os


class RaceGame:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()

        # -------------------
        # COLORS
        # -------------------
        self.GREEN = (34, 139, 34)
        self.ROAD_GRAY = (60, 60, 60)
        self.LINE_WHITE = (240, 240, 240)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 215, 0)

        # -------------------
        # FONT
        # -------------------
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 40)

        # -------------------
        # PATH
        # -------------------
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # -------------------
        # ASSETS
        # -------------------
        self.player_w, self.player_h = 70, 120
        self.enemy_w, self.enemy_h = 70, 120
        self.coin_size = 30

        self.player_img = pygame.transform.scale(
            pygame.image.load(os.path.join(self.BASE_DIR, "images", "player_car.png")),
            (self.player_w, self.player_h)
        )

        self.enemy_img = pygame.transform.scale(
            pygame.image.load(os.path.join(self.BASE_DIR, "images", "enemy_car.png")),
            (self.enemy_w, self.enemy_h)
        )

        self.coin_img = pygame.transform.scale(
            pygame.image.load(os.path.join(self.BASE_DIR, "images", "coin.png")),
            (self.coin_size, self.coin_size)
        )

        # -------------------
        # AUDIO
        # -------------------
        pygame.mixer.music.load(os.path.join(self.BASE_DIR, "sounds", "background_music.mp3"))
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

        self.coin_sound = pygame.mixer.Sound(os.path.join(self.BASE_DIR, "sounds", "coin_sound.mp3"))
        self.crash_sound = pygame.mixer.Sound(os.path.join(self.BASE_DIR, "sounds", "crash_sound.mp3"))
        self.speed_sound = pygame.mixer.Sound(os.path.join(self.BASE_DIR, "sounds", "speed_sound.mp3"))

        self.coin_sound.set_volume(0.9)
        self.crash_sound.set_volume(1.0)
        self.speed_sound.set_volume(0.7)

        # -------------------
        # GAME SETTINGS
        # -------------------
        self.player_speed = 6
        self.coin_speed = 5

        self.enemy_speed_base = 4
        self.enemy_speed = self.enemy_speed_base
        self.speed_increment = 0.15

        # 🎯 N coins threshold
        self.coin_boost_threshold = 5

        # prevents sound spam
        self.last_coin_milestone = 0

        self.game_over = False
        self.reset_game()

    # -------------------
    # RESET
    # -------------------
    def reset_game(self):
        ex = random.randint(0, self.WIDTH - self.enemy_w)

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

    # -------------------
    # COIN SPAWN
    # -------------------
    def spawn_coin(self, enemy_rect):
        while True:
            x = random.randint(0, self.WIDTH - self.coin_size)
            y = random.randint(-400, -100)

            coin_rect = pygame.Rect(x, y, self.coin_size, self.coin_size)

            if not coin_rect.colliderect(enemy_rect):
                return x, y

    # -------------------
    # INPUT
    # -------------------
    def handle_input(self, keys):
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed

        if keys[pygame.K_RIGHT] and self.player_x < self.WIDTH - self.player_w:
            self.player_x += self.player_speed

    # -------------------
    # UPDATE
    # -------------------
    def update(self):
        if self.game_over:
            return

        # enemy movement
        self.enemy_y += self.enemy_speed

        if self.enemy_y > self.HEIGHT:
            self.enemy_y = -150
            self.enemy_x = random.randint(0, self.WIDTH - self.enemy_w)

            self.score += 1
            self.enemy_speed += self.speed_increment

        enemy_rect = pygame.Rect(self.enemy_x, self.enemy_y, self.enemy_w, self.enemy_h)

        # coin movement
        self.coin_y += self.coin_speed

        if self.coin_y > self.HEIGHT:
            self.coin_x, self.coin_y = self.spawn_coin(enemy_rect)

        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_w, self.player_h)
        coin_rect = pygame.Rect(self.coin_x, self.coin_y, self.coin_size, self.coin_size)

        # crash
        if player_rect.colliderect(enemy_rect):
            self.crash_sound.play()
            self.game_over = True

        # coin collect
        if player_rect.colliderect(coin_rect):
            self.coins += 1
            self.coin_sound.play()
            self.coin_x, self.coin_y = self.spawn_coin(enemy_rect)

        # 🎯 COIN-BASED SPEED BOOST (FIXED)
        if self.coins != 0 and self.coins % self.coin_boost_threshold == 0:
            if self.coins != self.last_coin_milestone:
                self.enemy_speed += 0.25
                self.speed_sound.play()
                self.last_coin_milestone = self.coins

    # -------------------
    # DRAW
    # -------------------
    def draw(self):
        self.screen.fill(self.GREEN)

        pygame.draw.rect(self.screen, self.ROAD_GRAY, (80, 0, 200, self.HEIGHT))
        pygame.draw.line(self.screen, self.LINE_WHITE, (140, 0), (140, self.HEIGHT), 3)
        pygame.draw.line(self.screen, self.LINE_WHITE, (220, 0), (220, self.HEIGHT), 3)

        self.screen.blit(self.player_img, (self.player_x, self.player_y))
        self.screen.blit(self.enemy_img, (self.enemy_x, self.enemy_y))
        self.screen.blit(self.coin_img, (self.coin_x, self.coin_y))

        self.screen.blit(self.font.render(f"Score: {self.score}", True, self.BLACK), (10, 10))
        self.screen.blit(self.font.render(f"Coins: {self.coins}", True, self.BLACK), (10, 40))

        if self.game_over:
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            self.screen.blit(self.big_font.render("GAME OVER", True, self.YELLOW), (70, 180))
            self.screen.blit(self.font.render(f"Score: {self.score}", True, self.WHITE), (120, 260))
            self.screen.blit(self.font.render(f"Coins: {self.coins}", True, self.WHITE), (120, 300))
            self.screen.blit(self.font.render("R = Restart", True, self.YELLOW), (120, 380))
            self.screen.blit(self.font.render("Q = Quit", True, self.YELLOW), (130, 420))

    # -------------------
    # EVENTS
    # -------------------
    def handle_events(self, event):
        if self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_q:
                return False
        return True