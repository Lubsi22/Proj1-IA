import pygame

from Controller.Level import level


COLOR_MAP = {
    "red": (255,0,0),
    "green": (0,255,0),
    "blue": (0,0,255)
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
