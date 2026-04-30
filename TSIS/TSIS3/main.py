import pygame
import sys
from racer import RaceGame
from persistence import load_settings, load_leaderboard
from persistence import add_score
from ui import Button

pygame.init()

WIDTH, HEIGHT = 360, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)

MENU = "menu"
PLAY = "play"
GAME_OVER = "over"
LEADERBOARD = "leaderboard"

state = MENU

settings = load_settings()
leaderboard = load_leaderboard()
game = None


# ---------------- BUTTONS ----------------
play_btn = Button(90, 200, 180, 50, "PLAY", font)
lb_btn = Button(90, 270, 180, 50, "LEADERBOARD", font)
quit_btn = Button(90, 340, 180, 50, "QUIT", font)


def get_username():
    name = ""
    active = True

    while active:
        screen.fill((0, 0, 0))

        t = font.render("ENTER NAME:", True, (255, 255, 255))
        screen.blit(t, (80, 200))

        n = font.render(name, True, (0, 255, 255))
        screen.blit(n, (80, 260))

        hint = font.render("ENTER to confirm", True, (150, 150, 150))
        screen.blit(hint, (80, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode


# ---------------- MAIN LOOP ----------------
while True:
    clock.tick(60)
    screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ---------------- MENU ----------------
    if state == MENU:

        title = font.render("RACER GAME", True, (255, 255, 255))
        screen.blit(title, (90, 100))

        if play_btn.clicked():
            settings["username"] = get_username()
            game = RaceGame(screen, settings)
            state = PLAY

        if lb_btn.clicked():
            leaderboard = load_leaderboard()
            state = LEADERBOARD

        if quit_btn.clicked():
            pygame.quit()
            sys.exit()

        play_btn.draw(screen)
        lb_btn.draw(screen)
        quit_btn.draw(screen)

    # ---------------- GAME ----------------
    elif state == PLAY:
        keys = pygame.key.get_pressed()
        game.handle_input(keys)
        game.update()
        game.draw()

        if game.game_over:
            state = GAME_OVER

    # ---------------- GAME OVER ----------------

    elif state == GAME_OVER:
        screen.fill((0, 0, 0))

        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (100, 180))
        screen.blit(font.render(f"Score: {game.score}", True, (255, 255, 255)), (100, 240))

        retry = Button(90, 320, 180, 50, "RETRY", font)
        menu = Button(90, 390, 180, 50, "MENU", font)
        if not game.saved:
            add_score(settings["username"], game.score, game.distance)
            game.saved = True
            screen.blit(font.render("GAME OVER", True, (255,0,0)), (100, 200))
            screen.blit(font.render(f"Score: {game.score}", True, (255,255,255)), (100, 260))
            
        if retry.clicked():
            game = RaceGame(screen, settings)
            state = PLAY

        if menu.clicked():
            state = MENU

        retry.draw(screen)
        menu.draw(screen)

    # ---------------- LEADERBOARD ----------------
    elif state == LEADERBOARD:
        screen.fill((0, 0, 0))

        screen.blit(font.render("LEADERBOARD", True, (255, 255, 255)), (80, 80))

        y = 160
        for i, e in enumerate(leaderboard):
            txt = f"{i+1}. {e['name']} - {e['score']}"
            screen.blit(font.render(txt, True, (255, 255, 255)), (40, y))
            y += 40

        back = Button(90, 520, 180, 50, "BACK", font)

        if back.clicked():
            state = MENU

        back.draw(screen)

    pygame.display.flip()