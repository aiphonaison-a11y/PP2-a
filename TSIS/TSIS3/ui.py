# ui.py
import pygame
import json

class GameUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.WIDTH, self.HEIGHT = screen.get_size()

        self.font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)

        self.input_active = False
        self.temp_username = ""

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if self.game.game_state == "USERNAME" and self.input_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.temp_username.strip():
                    self.game.username = self.temp_username.strip()[:12]
                    self.input_active = False
                    self.game.reset_game()
                    self.game.game_state = "PLAYING"
                elif event.key == pygame.K_BACKSPACE:
                    self.temp_username = self.temp_username[:-1]
                elif event.unicode and len(self.temp_username) < 12:
                    self.temp_username += event.unicode
            return

        # Game Over keys
        if self.game.game_state == "GAME_OVER" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.reset_game()
                self.game.game_state = "PLAYING"
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                self.game.game_state = "MENU"
            return

        # Mouse clicks for menus
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse_click(*event.pos)

    def handle_mouse_click(self, mx, my):
        if self.game.game_state == "MENU":
            if 170 <= my <= 220:      # Play
                self.input_active = True
                self.temp_username = ""
                self.game.game_state = "USERNAME"
            elif 250 <= my <= 300:    # Leaderboard
                self.game.game_state = "LEADERBOARD"
            elif 330 <= my <= 380:    # Settings
                self.game.game_state = "SETTINGS"
            elif 410 <= my <= 460:    # Quit
                pygame.quit()
                quit()

        elif self.game.game_state == "LEADERBOARD":
            if my > 520:              # Back button
                self.game.game_state = "MENU"

        elif self.game.game_state == "SETTINGS":
            if 180 <= my <= 230:      # Sound
                self.game.settings["sound"] = not self.game.settings["sound"]
                self.game.save_settings()
            elif 270 <= my <= 320:    # Difficulty
                diffs = ["easy", "medium", "hard"]
                idx = diffs.index(self.game.settings.get("difficulty", "medium"))
                self.game.settings["difficulty"] = diffs[(idx + 1) % 3]
                self.game.save_settings()
            elif 420 <= my <= 470:    # Back
                self.game.game_state = "MENU"

    def draw(self):
        if self.game.game_state == "MENU":
            self.draw_menu()
        elif self.game.game_state == "USERNAME":
            self.draw_username()
        elif self.game.game_state == "PLAYING":
            self.game.draw()
        elif self.game.game_state == "GAME_OVER":
            self.game.draw()
            self.draw_game_over()
        elif self.game.game_state == "LEADERBOARD":
            self.draw_leaderboard()
        elif self.game.game_state == "SETTINGS":
            self.draw_settings()

    # ==================== DRAW METHODS ====================

    def draw_menu(self):
        self.screen.fill((28, 28, 48))
        title = self.big_font.render("RACER", True, (255, 215, 0))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 70))

        options = ["PLAY", "LEADERBOARD", "SETTINGS", "QUIT"]
        mouse_y = pygame.mouse.get_pos()[1]

        for i, text in enumerate(options):
            y = 180 + i * 70
            color = (100, 220, 255) if y - 10 < mouse_y < y + 40 else (220, 220, 220)
            surf = self.font.render(text, True, color)
            self.screen.blit(surf, (self.WIDTH//2 - surf.get_width()//2, y))

    def draw_username(self):
        self.screen.fill((20, 20, 40))
        t1 = self.big_font.render("ENTER YOUR NAME", True, (255, 255, 255))
        self.screen.blit(t1, (self.WIDTH//2 - t1.get_width()//2, 160))

        box = self.font.render(self.temp_username + "_", True, (255, 215, 0))
        self.screen.blit(box, (self.WIDTH//2 - box.get_width()//2, 280))

        hint = self.small_font.render("Press ENTER to start racing", True, (180,180,180))
        self.screen.blit(hint, (self.WIDTH//2 - hint.get_width()//2, 380))

    def draw_game_over(self):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        go = self.big_font.render("GAME OVER", True, (255, 60, 60))
        self.screen.blit(go, (self.WIDTH//2 - go.get_width()//2, 130))

        stats = [
            f"Final Score : {self.game.score}",
            f"Distance    : {self.game.distance//10} m",
            f"Coins       : {self.game.coins}"
        ]
        for i, line in enumerate(stats):
            txt = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(txt, (self.WIDTH//2 - txt.get_width()//2, 230 + i*50))

        self.screen.blit(self.font.render("R - Retry    Q - Main Menu", True, (200,200,200)), 
                        (self.WIDTH//2 - 140, 380))

    def draw_leaderboard(self):
        self.screen.fill((25, 25, 45))
        title = self.big_font.render("TOP 10", True, (255, 215, 0))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 50))

        try:
            with open("leaderboard.json") as f:
                board = json.load(f)
        except:
            board = []

        for i, entry in enumerate(board[:10]):
            text = f"{i+1:2d}. {entry['name']:<10} {entry['score']:6d}   {entry['distance']}m"
            color = (255, 240, 100) if i == 0 else (220, 220, 255)
            surf = self.small_font.render(text, True, color)
            self.screen.blit(surf, (35, 130 + i * 38))

        back = self.font.render("BACK", True, (255, 100, 100))
        self.screen.blit(back, (self.WIDTH//2 - 40, 540))

    def draw_settings(self):
        self.screen.fill((30, 30, 55))
        title = self.big_font.render("SETTINGS", True, (255, 215, 0))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 70))

        sound_status = "ON" if self.game.settings.get("sound", True) else "OFF"
        diff = self.game.settings.get("difficulty", "medium").upper()

        self.screen.blit(self.font.render(f"Sound: {sound_status}", True, (255,255,255)), (80, 180))
        self.screen.blit(self.font.render(f"Difficulty: {diff}", True, (255,255,255)), (80, 260))

        self.screen.blit(self.font.render("BACK", True, (255, 100, 100)), (self.WIDTH//2 - 45, 420))