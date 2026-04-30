import pygame
import datetime
from paint import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint App 2.0 + TSIS Tools Upgrade")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 18)

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    palette = create_color_palette(200, 60)
    palette_rect = pygame.Rect(WIDTH - 220, 20, 200, 60)

    current_tool = "brush"
    current_color = BLACK
    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None

    # TEXT TOOL STATE
    text_mode = False
    text_input = ""
    text_pos = (0, 0)

    # LINE PREVIEW
    preview_end = None

    running = True

    while running:
        screen.fill(WHITE)

        tool_buttons, color_buttons = draw_toolbar(
            screen, current_tool, current_color, brush_size,
            font, palette, palette_rect
        )

        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # ================= EVENTS =================
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # -------- KEYBOARD --------
            elif event.type == pygame.KEYDOWN:

                # SAVE
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = f"canvas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(canvas, filename)

                # TEXT INPUT MODE
                if text_mode:
                    if event.key == pygame.K_RETURN:
                        render_text(canvas, text_input, text_pos, font)
                        text_mode = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode

                else:
                    # TOOLS
                    if event.key == pygame.K_b:
                        current_tool = "brush"
                    elif event.key == pygame.K_p:
                        current_tool = "pencil"
                    elif event.key == pygame.K_l:
                        current_tool = "line"
                    elif event.key == pygame.K_r:
                        current_tool = "rectangle"
                    elif event.key == pygame.K_c:
                        current_tool = "circle"
                    elif event.key == pygame.K_e:
                        current_tool = "eraser"
                    elif event.key == pygame.K_f:
                        current_tool = "fill"
                    elif event.key == pygame.K_t:
                        current_tool = "text"

                    # BRUSH SIZE
                    elif event.key == pygame.K_1:
                        brush_size = 2
                    elif event.key == pygame.K_2:
                        brush_size = 5
                    elif event.key == pygame.K_3:
                        brush_size = 10

            # -------- MOUSE DOWN --------
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.pos[1] < TOOLBAR_HEIGHT:
                    for tool, rect in tool_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_tool = tool

                    for rect, color in color_buttons:
                        if rect.collidepoint(event.pos):
                            current_color = color

                    if palette_rect.collidepoint(event.pos):
                        px = event.pos[0] - palette_rect.x
                        py = event.pos[1] - palette_rect.y
                        current_color = palette.get_at((px, py))

                else:
                    drawing = True
                    start_pos = clamp_to_canvas(event.pos)
                    last_pos = start_pos

                    # TEXT TOOL
                    if current_tool == "text":
                        text_mode = True
                        text_pos = start_pos
                        text_input = ""

                    # FLOOD FILL TOOL
                    elif current_tool == "fill":
                        flood_fill(canvas, start_pos, current_color)

                    # PENCIL / BRUSH START
                    elif current_tool in ["brush", "pencil", "eraser"]:
                        color_used = current_color if current_tool != "eraser" else WHITE
                        pygame.draw.circle(canvas, color_used, start_pos, brush_size)

            # -------- MOUSE MOVE --------
            elif event.type == pygame.MOUSEMOTION and drawing:

                current_pos = clamp_to_canvas(event.pos)

                if current_tool in ["brush", "pencil", "eraser"]:
                    color_used = current_color if current_tool != "eraser" else WHITE
                    draw_brush(canvas, color_used, last_pos, current_pos, brush_size)

                elif current_tool == "line":
                    preview_end = current_pos

                last_pos = current_pos

            # -------- MOUSE UP --------
            elif event.type == pygame.MOUSEBUTTONUP:

                if start_pos:
                    end_pos = clamp_to_canvas(event.pos)

                    if current_tool == "line":
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                    elif current_tool == "rectangle":
                        pygame.draw.rect(canvas, current_color,
                                         pygame.Rect(start_pos,
                                                     (end_pos[0]-start_pos[0],
                                                      end_pos[1]-start_pos[1])),
                                         brush_size)

                    elif current_tool == "circle":
                        r = distance(start_pos, end_pos)
                        pygame.draw.circle(canvas, current_color, start_pos, r, brush_size)

                drawing = False
                start_pos = None
                last_pos = None
                preview_end = None

        # -------- LINE PREVIEW --------
        if current_tool == "line" and drawing and start_pos and preview_end:
            pygame.draw.line(screen, current_color,
                             (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT),
                             (preview_end[0], preview_end[1] + TOOLBAR_HEIGHT),
                             brush_size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()