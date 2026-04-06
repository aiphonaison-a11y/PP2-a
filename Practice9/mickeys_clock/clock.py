import pygame
import math
import time

class MickeyClock:
    def __init__(self, screen, center):
        self.screen = screen
        self.center = center
        self.hand_img = pygame.image.load("images/mickey_hand.png")
        self.hand_img = pygame.transform.scale(self.hand_img, (50, 150))

    def draw(self):
        current_time = time.localtime()
        seconds = current_time.tm_sec
        minutes = current_time.tm_min

        # Convert to angles
        sec_angle = -seconds * 6   # 360/60
        min_angle = -minutes * 6

        # Rotate images
        sec_hand = pygame.transform.rotate(self.hand_img, sec_angle)
        min_hand = pygame.transform.rotate(self.hand_img, min_angle)

        # Draw hands
        sec_rect = sec_hand.get_rect(center=self.center)
        min_rect = min_hand.get_rect(center=self.center)

        self.screen.blit(min_hand, min_rect)
        self.screen.blit(sec_hand, sec_rect)