import pygame
import random
import json
import os
from datetime import datetime

class RaceGame:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.load_assets()
        self.load_settings()
        self.reset_game()

        self.game_state = "MENU"
        self.username = "Player"

    def load_assets(self):
        def load_image(path, size):
            full = os.path.join(self.BASE_DIR, path)
            if not os.path.exists(full):
                surf = pygame.Surface(size, pygame.SRCALPHA)
                surf.fill((255, 0, 255))
                return surf
            img = pygame.image.load(full).convert_alpha()
            return pygame.transform.scale(img, size)

        def load_sound(path):
            full = os.path.join(self.BASE_DIR, path)
            return pygame.mixer.Sound(full) if os.path.exists(full) else None

        # Images with proper sizes
        self.player_img = load_image("assets/images/player_car.png", (70, 120))
        self.enemy_img = load_image("assets/images/enemy_car.png", (70, 120))
        
        self.barrier_img = load_image("assets/images/barrier.png", (75, 45))   # Wider barrier
        self.oil_img     = load_image("assets/images/oil.png",     (65, 65))   # Bigger oil spill
        self.nitro_img   = load_image("assets/images/speedup.png", (70, 35))

        # Coins - Bigger and consistent
        self.coin_imgs = {
            1:  load_image("assets/images/coin.png",      (36, 36)),
            5:  load_image("assets/images/blue_coin.png", (34, 34)),
            10: load_image("assets/images/pink_coin.png", (32, 32))
        }

        pygame.mixer.music.load(os.path.join(self.BASE_DIR, "assets/sounds/background_music.mp3"))
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

        self.coin_sound = load_sound("assets/sounds/coin_sound.mp3")
        self.crash_sound = load_sound("assets/sounds/crash_sound.mp3")
        self.speed_sound = load_sound("assets/sounds/speed_sound.mp3")

        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 42)

    def reset_game(self):
        self.player_x = self.WIDTH // 2 - 35
        self.player_y = self.HEIGHT - 180
        self.player_speed = 8.5

        self.distance = 0
        self.coins = 0
        self.score = 0
        self.game_over = False

        self.enemy_speed = 6.0
        self.coin_speed = 5.2

        self.obstacles = []
        self.powerups = []
        self.traffic = []

        self.power_up_active = None
        self.power_up_timer = 0
        self.shield_active = False

    # ==================== SPAWNING (Fixed Frequency) ====================

    def spawn_obstacle(self):
        # Reduced spawn rate + difficulty scaling
        spawn_chance = 0.022 + (self.distance / 12000)
        if random.random() < spawn_chance:
            x = random.randint(45, self.WIDTH - 115)
            obs_type = random.choice(["barrier", "oil"])
            self.obstacles.append({"x": x, "y": -100, "type": obs_type})

    def spawn_powerup(self):
        if random.random() < 0.014:        # Quite rare - good balance
            x = random.randint(55, self.WIDTH - 105)
            ptype = random.choice(["nitro", "shield", "repair"])
            self.powerups.append({"x": x, "y": -90, "type": ptype, "life": 500})

    def spawn_traffic(self):
        if len(self.traffic) < 3 and random.random() < 0.038 + (self.distance / 9000):
            x = random.randint(45, self.WIDTH - 115)
            speed = self.enemy_speed + random.uniform(-1.0, 1.5)
            self.traffic.append({"x": x, "y": -180, "speed": speed})

    def update(self):
        if self.game_state != "PLAYING" or self.game_over:
            return

        self.distance += 1
        self.score = int(self.distance / 7) + self.coins * 10

        # Gradual difficulty
        self.enemy_speed = 6.0 + self.distance / 850
        self.coin_speed = 5.2 + self.distance / 1300

        self.spawn_obstacle()
        self.spawn_powerup()
        self.spawn_traffic()

        # Update moving objects
        for t in self.traffic[:]:
            t["y"] += t["speed"]
            if t["y"] > self.HEIGHT + 100:
                self.traffic.remove(t)

        for o in self.obstacles[:]:
            o["y"] += self.coin_speed
            if o["y"] > self.HEIGHT + 50:
                self.obstacles.remove(o)

        for p in self.powerups[:]:
            p["y"] += self.coin_speed
            p["life"] -= 1
            if p["y"] > self.HEIGHT or p["life"] <= 0:
                self.powerups.remove(p)

        self.check_collisions()

        # Power-up timer
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.power_up_active = None
                self.player_speed = 8.5

    def check_collisions(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, 70, 120)

        # === Traffic Collision ===
        for t in self.traffic[:]:
            t_rect = pygame.Rect(t["x"], t["y"], 70, 120)
            if player_rect.colliderect(t_rect):
                if self.shield_active:
                    self.shield_active = False
                    self.traffic.remove(t)
                    continue
                self.crash()
                return

        # === Obstacles Collision ===
        for o in self.obstacles[:]:
            if o["type"] == "barrier":
                o_rect = pygame.Rect(o["x"], o["y"], 75, 45)
            else:  # oil
                o_rect = pygame.Rect(o["x"], o["y"], 65, 65)

            if player_rect.colliderect(o_rect):
                if self.shield_active:
                    self.shield_active = False
                    self.obstacles.remove(o)
                    continue
                if o["type"] == "oil":
                    self.player_speed = 4.0   # slow down
                else:
                    self.crash()
                    return

        # === Power-up Collection ===
        for p in self.powerups[:]:
            p_rect = pygame.Rect(p["x"], p["y"], 50, 50)
            if player_rect.colliderect(p_rect):
                self.collect_powerup(p["type"])
                if p in self.powerups:
                    self.powerups.remove(p)

    def collect_powerup(self, ptype):
        if ptype == "nitro":
            self.power_up_active = "nitro"
            self.power_up_timer = 210   # 3.5 seconds
            self.player_speed = 15.5
        elif ptype == "shield":
            self.shield_active = True
            self.power_up_active = "shield"
            self.power_up_timer = 480
        elif ptype == "repair":
            self.coins += 10
            # Remove first obstacle if exists
            if self.obstacles:
                self.obstacles.pop(0)

    def crash(self):
        if self.crash_sound:
            self.crash_sound.play()
        self.game_over = True
        self.game_state = "GAME_OVER"
        self.save_to_leaderboard()

    def save_to_leaderboard(self):
        try:
            with open("leaderboard.json", "r") as f:
                board = json.load(f)
        except:
            board = []

        entry = {
            "name": self.username,
            "score": self.score,
            "distance": self.distance // 10,
            "coins": self.coins,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        board.append(entry)
        board.sort(key=lambda x: x["score"], reverse=True)
        with open("leaderboard.json", "w") as f:
            json.dump(board[:10], f, indent=2)

    def draw(self):
        self.screen.fill((55, 55, 65))

        # Road lines
        pygame.draw.line(self.screen, (240, 240, 240), (118, 0), (118, self.HEIGHT), 7)
        pygame.draw.line(self.screen, (240, 240, 240), (242, 0), (242, self.HEIGHT), 7)

        # Traffic
        for t in self.traffic:
            self.screen.blit(self.enemy_img, (t["x"], t["y"]))

        # Obstacles
        for o in self.obstacles:
            if o["type"] == "barrier":
                self.screen.blit(self.barrier_img, (o["x"], o["y"]))
            else:
                self.screen.blit(self.oil_img, (o["x"], o["y"]))

        # Power-ups
        for p in self.powerups:
            colors = {"nitro": (255, 70, 70), "shield": (70, 180, 255), "repair": (70, 255, 100)}
            color = colors.get(p["type"], (255, 255, 100))
            pygame.draw.rect(self.screen, color, (p["x"], p["y"], 48, 48), border_radius=8)
            label = self.font.render(p["type"][0].upper(), True, (0,0,0))
            self.screen.blit(label, (p["x"] + 17, p["y"] + 10))

        # Player Car
        self.screen.blit(self.player_img, (self.player_x, self.player_y))

        # HUD
        self.screen.blit(self.font.render(f"Dist: {self.distance//10}m", True, (255,255,255)), (12, 10))
        self.screen.blit(self.font.render(f"Coins: {self.coins}", True, (255, 220, 0)), (12, 38))
        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255, 240, 80)), (12, 66))

        if self.power_up_active:
            col = (255,80,80) if self.power_up_active == "nitro" else (100,220,255)
            self.screen.blit(self.font.render(f"{self.power_up_active.upper()} {self.power_up_timer//60}s", True, col), (WIDTH-195, 12))

        if self.shield_active:
            self.screen.blit(self.font.render("SHIELD ON", True, (100, 255, 255)), (WIDTH-185, 48))