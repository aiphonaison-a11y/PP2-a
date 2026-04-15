import pygame
 
 
class Ball:
    RADIUS = 25          # diameter = 50 px
    STEP   = 20          # Each key press moves the ball 20 px
    COLOR  = (220, 40, 40)   # Red ball
    OUTLINE= (160, 20, 20)   # Darker outline
 
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_w = screen_width
        self.screen_h = screen_height
 
        # Start the ball at the center of the screen
        self.x = screen_width  // 2
        self.y = screen_height // 2
 

    # Movement
    def move(self, dx: int, dy: int):
        new_x = self.x + dx
        new_y = self.y + dy
 
        # Clamp
        if self.RADIUS <= new_x <= self.screen_w - self.RADIUS:
            self.x = new_x
        if self.RADIUS <= new_y <= self.screen_h - self.RADIUS:
            self.y = new_y
 
    def move_up(self):    self.move(0, -self.STEP)
    def move_down(self):  self.move(0,  self.STEP)
    def move_left(self):  self.move(-self.STEP, 0)
    def move_right(self): self.move( self.STEP, 0)
 

    # Drawing

    def draw(self, surface: pygame.Surface):
        center = (int(self.x), int(self.y))
 
        # Shadow
        shadow_center = (center[0] + 3, center[1] + 3)
        pygame.draw.circle(surface, (200, 200, 200), shadow_center, self.RADIUS)
 
        # Main ball
        pygame.draw.circle(surface, self.COLOR, center, self.RADIUS)
 
        # Outline
        pygame.draw.circle(surface, self.OUTLINE, center, self.RADIUS, 2)
 
        # Small highlight dot (top-left)
        highlight = (center[0] - self.RADIUS // 3, center[1] - self.RADIUS // 3)
        pygame.draw.circle(surface, (255, 120, 120), highlight, self.RADIUS // 5)
 