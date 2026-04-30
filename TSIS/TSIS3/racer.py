import pygame
import random
import os


class RaceGame:
    def __init__(self, screen, settings):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.settings = settings

        BASE = os.path.dirname(os.path.abspath(__file__))

        def img(path, size):
            return pygame.transform.scale(
                pygame.image.load(os.path.join(BASE, path)).convert_alpha(),
                size
            )

        def sound(path):
            return pygame.mixer.Sound(os.path.join(BASE, path))

        # ---------------- ASSETS ----------------
        self.player = img("assets/images/player_car.png", (60, 100))
        self.enemy = img("assets/images/enemy_car.png", (60, 100))

        self.coin = img("assets/images/coin.png", (25, 25))
        self.blue_coin = img("assets/images/blue_coin.png", (25, 25))
        self.pink_coin = img("assets/images/pink_coin.png", (25, 25))

        self.oil = img("assets/images/oil.png", (70, 70))
        self.barrier = img("assets/images/barrier.png", (60, 100))
        self.pothole = img("assets/images/pothole.png", (60, 60))

        # ---------------- SOUNDS ----------------
        self.coin_s = sound("assets/sounds/coin_sound.mp3")
        self.crash_s = sound("assets/sounds/crash_sound.mp3")

        pygame.mixer.music.load(os.path.join(BASE, "assets/sounds/background_music.mp3"))
        pygame.mixer.music.play(-1)

        # ---------------- PLAYER ----------------
        self.x = self.WIDTH // 2
        self.y = self.HEIGHT - 140

        self.speed = 7
        self.normal_speed = 7

        # oil slow system
        self.slow_timer = 0

        self.reset()

        diff = self.settings.get("difficulty", "normal")
        self.spawn_rate = 55 if diff == "easy" else 40 if diff == "normal" else 30

    # ---------------- RESET ----------------
    def reset(self):
        self.enemies = []
        self.obstacles = []

        self.coin_x, self.coin_y, self.coin_type = self.spawn_coin()

        self.score = 0
        self.coins = 0
        self.distance = 0

        self.spawn_timer = 0
        self.game_over = False
        self.saved = False

        self.slow_timer = 0
        self.speed = self.normal_speed

    # ---------------- COIN SPAWN ----------------
    def spawn_coin(self):
        x = random.randint(40, self.WIDTH - 40)
        y = random.randint(-400, -50)
        coin_type = random.choice(["yellow", "blue", "pink"])
        return x, y, coin_type

    # ---------------- SPAWN ----------------
    def spawn(self):
        x = random.randint(40, self.WIDTH - 80)
        r = random.randint(1, 100)

        if r < 50:
            self.enemies.append(pygame.Rect(x, -120, 60, 100))
        else:
            t = random.choice(["oil", "barrier", "pothole"])
            if t == "oil":
                rect = pygame.Rect(x, -100, 70, 70)
            elif t == "barrier":
                rect = pygame.Rect(x, -120, 60, 100)
            else:
                rect = pygame.Rect(x, -100, 60, 60)
            self.obstacles.append((rect, t))

    # ---------------- INPUT ----------------
    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

    # ---------------- UPDATE ----------------
    def update(self):
        # ---------------- GAME OVER STOP ----------------
        if self.game_over:
            return

        # ---------------- OIL RECOVERY SYSTEM ----------------
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer == 0:
                self.speed = self.normal_speed

        self.distance += self.speed
        self.score = self.coins * 10 + self.distance // 10

        # spawn logic
        self.spawn_timer += 1
        if self.spawn_timer > self.spawn_rate:
            self.spawn()
            self.spawn_timer = 0

        # move enemies
        for e in self.enemies:
            e.y += self.speed

        # move obstacles
        for i in range(len(self.obstacles)):
            r, t = self.obstacles[i]
            r.y += self.speed
            self.obstacles[i] = (r, t)

        # coin move
        self.coin_y += self.speed
        if self.coin_y > self.HEIGHT:
            self.coin_x, self.coin_y, self.coin_type = self.spawn_coin()

        player_rect = pygame.Rect(self.x, self.y, 60, 100)
        coin_rect = pygame.Rect(self.coin_x, self.coin_y, 25, 25)

        # ---------------- COIN COLLECT ----------------
        if player_rect.colliderect(coin_rect):
            self.coin_s.play()

            if self.coin_type == "yellow":
                self.coins += 1
            elif self.coin_type == "blue":
                self.coins += 3
            else:
                self.coins += 5

            self.coin_x, self.coin_y, self.coin_type = self.spawn_coin()

        # ---------------- ENEMY COLLISION ----------------
        for e in self.enemies:
            if player_rect.colliderect(e):
                self.crash_s.play()
                self.game_over = True

        # ---------------- OBSTACLES ----------------
        for o, t in self.obstacles:
            if player_rect.colliderect(o):
                if t == "barrier":
                    self.crash_s.play()
                    self.game_over = True
                elif t == "oil":
                    self.speed = 3
                    self.slow_timer = 60  # temporary slow (~1 sec)

    # ---------------- DRAW ----------------
    def draw(self):
        self.screen.fill((40, 40, 40))

        pygame.draw.line(self.screen, (255, 255, 255), (120, 0), (120, self.HEIGHT), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (240, 0), (240, self.HEIGHT), 3)

        self.screen.blit(self.player, (self.x, self.y))

        for e in self.enemies:
            self.screen.blit(self.enemy, e.topleft)

        for o, t in self.obstacles:
            if t == "oil":
                self.screen.blit(self.oil, o.topleft)
            elif t == "barrier":
                self.screen.blit(self.barrier, o.topleft)
            else:
                self.screen.blit(self.pothole, o.topleft)

        if self.coin_type == "yellow":
            img = self.coin
        elif self.coin_type == "blue":
            img = self.blue_coin
        else:
            img = self.pink_coin

        self.screen.blit(img, (self.coin_x, self.coin_y))

        f = pygame.font.SysFont("Arial", 20)
        self.screen.blit(f.render(f"Score:{self.score}", True, (255,255,255)), (10,10))
        self.screen.blit(f.render(f"Coins:{self.coins}", True, (255,255,0)), (10,35))