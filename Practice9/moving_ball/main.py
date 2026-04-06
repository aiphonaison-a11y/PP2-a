import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ball = Ball(300, 200, 25, WIDTH, HEIGHT)

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        ball.move(0, -20)
    if keys[pygame.K_DOWN]:
        ball.move(0, 20)
    if keys[pygame.K_LEFT]:
        ball.move(-20, 0)
    if keys[pygame.K_RIGHT]:
        ball.move(20, 0)

    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()