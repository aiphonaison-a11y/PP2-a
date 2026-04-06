class Ball:
    def __init__(self, x, y, radius, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 20
        self.sw = screen_width
        self.sh = screen_height

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if self.radius <= new_x <= self.sw - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.sh - self.radius:
            self.y = new_y