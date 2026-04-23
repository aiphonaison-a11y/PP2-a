import pygame
import sys
from race import RaceGame

pygame.init()

WIDTH, HEIGHT = 360, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Dodge Game")

clock = pygame.time.Clock()
FPS = 60

game = RaceGame(screen)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        running = game.handle_events(event)

    keys = pygame.key.get_pressed()
    game.handle_input(keys)
    game.update()
    game.draw()

    pygame.display.update()

pygame.quit()
sys.exit()