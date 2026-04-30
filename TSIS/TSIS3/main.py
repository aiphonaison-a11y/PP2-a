import pygame
import sys
from racer import RaceGame
from ui import GameUI

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

WIDTH, HEIGHT = 360, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer 2.0 - TSIS 3")

clock = pygame.time.Clock()
FPS = 60

game = RaceGame(screen)
ui = GameUI(screen, game)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ui.handle_event(event)

    keys = pygame.key.get_pressed()
    game.handle_input(keys)

    game.update()
    ui.update()
    ui.draw()

    pygame.display.update()

pygame.quit()
sys.exit()