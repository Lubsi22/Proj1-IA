import pygame

COLOR_MAP = {
    "red":    (255, 0,   0),
    "green":  (0,   255, 0),
    "blue":   (0,   0,   255),
    "yellow": (255, 220, 0),
    "purple": (148, 0,   211),
    "orange": (255, 140, 0),
    "cyan":   (0,   220, 220),
    "pink":   (255, 105, 180),
    "teal":   (0,   180, 160),
    "lime":   (160, 230, 0),
    "brown":  (139, 90,  43),
}

def draw_level(screen, bottles):
    for bottle in bottles:
        draw_bottle(screen, bottle)


def draw_bottle(screen, bottle):
    cords = bottle.cords
    pygame.draw.lines(screen, (255, 255, 255), False, cords, 2)

    draw_color(screen, cords, bottle.colors)


def draw_color(screen, cords, colors):
    x = cords[0][0]
    y_top = cords[0][1]
    y_bottom = cords[1][1]
    width = cords[3][0] - cords[0][0]

    height = y_bottom - y_top
    layer_height = height // 4

    # draw water layers (bottom up)
    for i, color in enumerate(colors):
        rgb = COLOR_MAP[color]

        rect = pygame.Rect(
            x + 2,
            y_bottom - layer_height * (i + 1),
            width - 4,
            layer_height
        )

        pygame.draw.rect(screen, rgb, rect)

def draw_level_buttons(screen, buttons):

    font = pygame.font.Font(None, 36)
    player_label = font.render("Player:", True, (255, 255, 255))
    screen.blit(player_label, (100, 10))

    color = (0,0,255)

    for btn in buttons:
        draw_button(screen, btn["text"], btn["rect"], color)


def draw_button(screen, text, rect, color, text_color=(255, 255, 255)):
    font = pygame.font.Font(None, 36)
    
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))

def draw_algorithm_buttons(screen, buttons):

    font = pygame.font.Font(None, 36)
    pc_label = font.render("PC:", True, (255, 255, 255))
    screen.blit(pc_label, (400, 10)) # chuzz ter de mudar aqui e no Button

    color = (0,0,255)

    for btn in buttons:
        draw_button(screen, btn["text"], btn["rect"], color)

