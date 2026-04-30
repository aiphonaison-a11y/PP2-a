import pygame

class Button:
    def __init__(self, x, y, w, h, text, font,
                 color=(70,70,70), hover=(130,130,130)):

        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.font = font
        self.color = color
        self.hover = hover
        self.pressed = False

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        col = self.hover if self.rect.collidepoint(mouse) else self.color
        pygame.draw.rect(screen, col, self.rect, border_radius=8)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2, border_radius=8)

        txt = self.font.render(self.text, True, (255,255,255))
        screen.blit(txt, (
            self.rect.centerx - txt.get_width()//2,
            self.rect.centery - txt.get_height()//2
        ))

    def clicked(self):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse):
            if pressed and not self.pressed:
                self.pressed = True
                return True

        if not pressed:
            self.pressed = False

        return False