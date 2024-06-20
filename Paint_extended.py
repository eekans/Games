import pygame

pygame.init()

fps = 60
timer = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
active_size = 0
active_color = 'white'
active_tool = 'line'

font = pygame.font.SysFont("Verdana", 20)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Paint")
painting = []

def draw_menu():
    pygame.draw.rect(screen, 'gray', [0, 0, WIDTH, 70])
    pygame.draw.line(screen, 'black', (0, 70), (WIDTH, 70), 3)

    line_brush = pygame.draw.rect(screen, 'black', [10, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 35), 5)

    eraser_brush = pygame.draw.rect(screen, 'black', [70, 10, 50, 50])
    pygame.draw.circle(screen, 'red', (95, 35), 5)

    rectangle_figure = pygame.draw.rect(screen, 'black', [130, 10, 50, 50])
    pygame.draw.rect(screen, 'white', pygame.Rect(140, 25, 30, 15))

    circle_figure = pygame.draw.rect(screen, 'black', [190, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (215, 35), 20, 3)

    square_figure = pygame.draw.rect(screen, 'black', [250, 10, 50, 50])
    pygame.draw.rect(screen, 'white', pygame.Rect(265, 25, 20, 20))

    triangleRIGHT_figure = pygame.draw.rect(screen, 'black', [310, 10, 50, 50])
    tr_txt = font.render("tr", True, 'white')
    screen.blit(tr_txt, (325, 20))

    triangleEQUIL_figure = pygame.draw.rect(screen, 'black', [370, 10, 50, 50])
    te_txt = font.render("te", True, 'white')
    screen.blit(te_txt, (385, 20))

    rhombus_figure = pygame.draw.rect(screen, 'black', [430, 10, 50, 50])
    rh_txt = font.render("rh", True, 'white')
    screen.blit(rh_txt, (445, 20))

    brush_list = [line_brush, eraser_brush, rectangle_figure, circle_figure, square_figure,
                  triangleRIGHT_figure, triangleEQUIL_figure, rhombus_figure]

    blue = pygame.draw.rect(screen, (0, 0, 255), [WIDTH - 35, 10, 25, 25])
    red = pygame.draw.rect(screen, (255, 0, 0), [WIDTH - 35, 35, 25, 25])
    green = pygame.draw.rect(screen, (0, 255, 0), [WIDTH - 60, 10, 25, 25])
    yellow = pygame.draw.rect(screen, (255, 255, 0), [WIDTH - 60, 35, 25, 25])
    teal = pygame.draw.rect(screen, (0, 255, 255), [WIDTH - 85, 10, 25, 25])
    purple = pygame.draw.rect(screen, (255, 0, 255), [WIDTH - 85, 35, 25, 25])
    grey = pygame.draw.rect(screen, (128, 128, 128), [WIDTH - 110, 10, 25, 25])
    black = pygame.draw.rect(screen, (0, 0, 0), [WIDTH - 110, 35, 25, 25])

    color_rect = [blue, red, green, yellow, teal, purple, grey, black]
    rgb_list = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0),
                (0, 255, 255), (255, 0, 255), (128, 128, 128), (0, 0, 0)]

    return brush_list, color_rect, rgb_list

def draw_painting(paints):
    for paint in paints:
        color, pos, size, shape = paint
        if shape == 'circle':
            pygame.draw.circle(screen, color, pos, size, 1)
        elif shape == 'line':
            pygame.draw.circle(screen, color, pos, size)
        elif shape == 'rectangle':
            x, y = pos
            pygame.draw.rect(screen, color, (x, y, size, size))
        elif shape == 'square':
            x, y = pos
            pygame.draw.rect(screen, color, (x, y, size, size))
        elif shape == "rhombus":
            x, y = pos
            half_size = size // 2
            vertices = [(x + half_size, y), (x, y + half_size), (x - half_size, y), (x, y - half_size)]
            pygame.draw.polygon(screen, color, vertices)
        elif shape == "triangle_equil":
            x, y = pos
            height = (3 ** 0.5 / 2) * size
            vertices = [(x, y - height / 2), (x - size / 2, y + height / 2), (x + size / 2, y + height / 2)]
            pygame.draw.polygon(screen, color, vertices)
        elif shape == "triangle_right":
            x, y = pos
            vertices = [(x - size / 2, y + size / 2), (x - size / 2, y - size / 2), (x + size / 2, y + size / 2)]
            pygame.draw.polygon(screen, color, vertices)


run = True
while run:
    timer.tick(fps)
    screen.fill('white')

    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
        active_size += 1
    elif keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        active_size = max(1, active_size - 1)

    if mouse[1] > 70:
        half_size = active_size / 2
        if active_tool in ['line', 'circle']:
            pygame.draw.circle(screen, active_color, mouse, active_size, 1 if active_tool == 'circle' else 0)
        elif active_tool == 'rectangle':
            pygame.draw.rect(screen, active_color, (mouse[0], mouse[1], active_size + 10, active_size))
        elif active_tool == 'square':
            x, y = mouse[0] - half_size, mouse[1] - half_size
            pygame.draw.rect(screen, active_color, (x, y, active_size, active_size))
        elif active_tool in ['triangle_equil', 'triangle_right']:
            height = (3 ** 0.5 / 2) * active_size
            vertices = [(mouse[0], mouse[1] - height / 2), (mouse[0] - active_size / 2, mouse[1] + height / 2),
                        (mouse[0] + active_size / 2, mouse[1] + height / 2)]
            if active_tool == 'triangle_right':
                vertices = [(mouse[0] - active_size / 2, mouse[1] + active_size / 2),
                            (mouse[0] - active_size / 2, mouse[1] - active_size / 2),
                            (mouse[0] + active_size / 2, mouse[1] + active_size / 2)]
            pygame.draw.polygon(screen, active_color, vertices)
        elif active_tool == 'rhombus':
            half_size = active_size // 2
            vertices = [(mouse[0] + half_size, mouse[1]), (mouse[0], mouse[1] + half_size),
                        (mouse[0] - half_size, mouse[1]), (mouse[0], mouse[1] - half_size)]
            pygame.draw.polygon(screen, active_color, vertices)

    if left_click and mouse[1] > 70:
        painting.append((active_color, mouse, active_size, active_tool))

    draw_painting(painting)
    brushes, colors, rgbs = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(brushes)):
                if brushes[0].collidepoint(event.pos):
                    active_size = 15
                    active_tool = 'line'
                elif brushes[1].collidepoint(event.pos):
                    active_color = 'white'
                    active_tool = 'line'
                elif brushes[2].collidepoint(event.pos):
                    active_tool = 'rectangle'
                elif brushes[3].collidepoint(event.pos):
                    active_tool = 'circle'
                elif brushes[4].collidepoint(event.pos):
                    active_tool = 'square'
                elif brushes[5].collidepoint(event.pos):
                    active_tool = 'triangle_right'
                elif brushes[6].collidepoint(event.pos):
                    active_tool = 'triangle_equil'
                elif brushes[7].collidepoint(event.pos):
                    active_tool = 'rhombus'

            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]

    pygame.display.flip()
