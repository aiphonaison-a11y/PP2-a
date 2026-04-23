import pygame
import colorsys


# Settings

WIDTH, HEIGHT = 900, 650
TOOLBAR_HEIGHT = 90
CANVAS_Y = TOOLBAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 140, 0)

COLOR_OPTIONS = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]


# Helpers

def draw_text(screen, text, x, y, font, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def make_rect(x, y, w, h):
    return pygame.Rect(x, y, w, h)


def normalize_rect(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    return pygame.Rect(min(x1, x2), min(y1, y2),
                       abs(x1 - x2), abs(y1 - y2))


# Rainbow color picker HSV
def create_color_palette(width, height):
    palette = pygame.Surface((width, height))
    for x in range(width):
        for y in range(height):
            h = x / width
            s = 1
            v = 1 - (y / height)

            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            palette.set_at((x, y), (int(r * 255), int(g * 255), int(b * 255)))
    return palette


def draw_brush(surface, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(steps + 1):
        x = int(start[0] + dx * i / steps)
        y = int(start[1] + dy * i / steps)
        pygame.draw.circle(surface, color, (x, y), radius)


def clamp_to_canvas(pos):
    x, y = pos
    return max(0, min(WIDTH - 1, x)), max(CANVAS_Y, min(HEIGHT - 1, y))



# Toolbar

def draw_toolbar(screen, current_tool, current_color, brush_size,
                 font, palette, palette_rect):

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    tools = ["brush", "rectangle", "circle", "eraser", "clear"]
    tool_buttons = {}

    x = 10
    for tool in tools:
        rect = make_rect(x, 10, 110, 30)
        tool_buttons[tool] = rect

        pygame.draw.rect(screen,
                         DARK_GRAY if current_tool == tool else WHITE,
                         rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        draw_text(screen, tool.capitalize(),
                  rect.x + 10, rect.y + 5, font,
                  WHITE if current_tool == tool else BLACK)

        x += 120

    # preset colors
    color_buttons = []
    x = 10
    y = 50
    for color in COLOR_OPTIONS:
        rect = make_rect(x, y, 35, 25)
        color_buttons.append((rect, color))

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 4 if color == current_color else 2)
        x += 45

    # palette
    screen.blit(palette, palette_rect.topleft)
    pygame.draw.rect(screen, BLACK, palette_rect, 2)

    # current color preview
    pygame.draw.rect(screen, current_color, (WIDTH - 60, 20, 40, 40))
    pygame.draw.rect(screen, BLACK, (WIDTH - 60, 20, 40, 40), 2)

    draw_text(screen, f"Size: {brush_size}", 360, 52, font)
    draw_text(screen, "B R C E | +/- size", 480, 20, font)

    return tool_buttons, color_buttons




# MAIN

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint App (finally not sad colors)")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 20)

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    # 🎨 palette
    palette = create_color_palette(200, 60)
    palette_rect = pygame.Rect(WIDTH - 220, 20, 200, 60)

    current_tool = "brush"
    current_color = BLACK
    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None

    running = True
    while running:
        screen.fill(WHITE)

        tool_buttons, color_buttons = draw_toolbar(
            screen, current_tool, current_color, brush_size,
            font, palette, palette_rect
        )

        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_b:
                    current_tool = "brush"
                elif event.key == pygame.K_r:
                    current_tool = "rectangle"
                elif event.key == pygame.K_c:
                    current_tool = "circle"
                elif event.key == pygame.K_e:
                    current_tool = "eraser"
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    brush_size = min(50, brush_size + 1)
                elif event.key == pygame.K_MINUS:
                    brush_size = max(1, brush_size - 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < TOOLBAR_HEIGHT:

                    # tools
                    for tool, rect in tool_buttons.items():
                        if rect.collidepoint(event.pos):
                            if tool == "clear":
                                canvas.fill(WHITE)
                            else:
                                current_tool = tool

                    # preset colors
                    for rect, color in color_buttons:
                        if rect.collidepoint(event.pos):
                            current_color = color

                    # 🌈 palette click
                    if palette_rect.collidepoint(event.pos):
                        px = event.pos[0] - palette_rect.x
                        py = event.pos[1] - palette_rect.y
                        current_color = palette.get_at((px, py))

                else:
                    drawing = True
                    start_pos = clamp_to_canvas(event.pos)
                    last_pos = start_pos

                    cpos = (start_pos[0], start_pos[1] - TOOLBAR_HEIGHT)

                    if current_tool == "brush":
                        pygame.draw.circle(canvas, current_color, cpos, brush_size)
                    elif current_tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, cpos, brush_size)

            elif event.type == pygame.MOUSEMOTION and drawing:
                current_pos = clamp_to_canvas(event.pos)

                c_last = (last_pos[0], last_pos[1] - TOOLBAR_HEIGHT)
                c_curr = (current_pos[0], current_pos[1] - TOOLBAR_HEIGHT)

                if current_tool == "brush":
                    draw_brush(canvas, current_color, c_last, c_curr, brush_size)
                elif current_tool == "eraser":
                    draw_brush(canvas, WHITE, c_last, c_curr, brush_size)

                last_pos = current_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                start_pos = None
                last_pos = None

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()