import pygame

BOTTLE_OUTLINE = (255, 255, 255)
BOTTLE_LINE_WIDTH = 2
BOTTLE_CORNER_RADIUS = 16

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

def draw_level(screen, bottles, selected_bottle=None):
    for bottle in bottles:
        draw_bottle(screen, bottle, is_selected=(bottle == selected_bottle))


def draw_move_counter(screen, move_count, total_moves=None):
    font = pygame.font.Font(None, 36)

    if total_moves is None:
        text = f"Moves: {move_count}"
    else:
        text = f"Moves: {move_count}/{total_moves}"

    label = font.render(text, True, (255, 255, 255))
    padding = 16
    rect = label.get_rect(topright=(screen.get_width() - padding, padding))
    background = rect.inflate(20, 14)

    pygame.draw.rect(screen, (25, 25, 25), background, border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), background, width=2, border_radius=8)
    screen.blit(label, rect)


def draw_bottle(screen, bottle, is_selected=False):
    x = bottle.x
    y_top = bottle.y
    width = bottle.width
    height = bottle.height

    outer_rect = pygame.Rect(x, y_top, width, height)

    # Draw liquid first so the glass outline stays visible in front.
    draw_color(screen, bottle)

    # Rounded container with an open top.
    pygame.draw.rect(
        screen,
        BOTTLE_OUTLINE,
        outer_rect,
        width=BOTTLE_LINE_WIDTH,
        border_bottom_left_radius=BOTTLE_CORNER_RADIUS,
        border_bottom_right_radius=BOTTLE_CORNER_RADIUS,
    )
    pygame.draw.line(screen, (0, 0, 0), outer_rect.topleft, outer_rect.topright, BOTTLE_LINE_WIDTH + 2)

    if is_selected:
        pulse = (pygame.time.get_ticks() // 220) % 2
        halo_color = (255, 215, 0) if pulse == 0 else (255, 240, 130)
        halo_rect = outer_rect.inflate(16, 20)
        pygame.draw.rect(
            screen,
            halo_color,
            halo_rect,
            width=3,
            border_bottom_left_radius=BOTTLE_CORNER_RADIUS + 8,
            border_bottom_right_radius=BOTTLE_CORNER_RADIUS + 8,
        )

        marker_x = outer_rect.centerx
        marker_top = outer_rect.top - 18
        pygame.draw.polygon(
            screen,
            halo_color,
            [(marker_x, marker_top), (marker_x - 8, marker_top + 12), (marker_x + 8, marker_top + 12)],
        )


def draw_color(screen, bottle):
    colors = bottle.colors
    if not colors:
        return

    x = bottle.x
    y_top = bottle.y
    width = bottle.width
    y_bottom = y_top + bottle.height

    layer_slots = max(1, bottle.visual_capacity)
    layer_height = bottle.height // layer_slots

    inner_x = x + 3
    inner_width = max(1, width - 6)
    clip_rect = pygame.Rect(inner_x, y_top + 2, inner_width, bottle.height - 2)

    prev_clip = screen.get_clip()
    screen.set_clip(clip_rect)

    # draw water layers (bottom up)
    for i, color in enumerate(colors):
        rgb = COLOR_MAP[color]

        rect = pygame.Rect(
            inner_x,
            y_bottom - layer_height * (i + 1),
            inner_width,
            layer_height
        )

        if i == 0:
            pygame.draw.rect(
                screen,
                rgb,
                rect,
                border_bottom_left_radius=max(0, BOTTLE_CORNER_RADIUS - 2),
                border_bottom_right_radius=max(0, BOTTLE_CORNER_RADIUS - 2),
            )
        else:
            pygame.draw.rect(screen, rgb, rect)

    screen.set_clip(prev_clip)


def draw_level_buttons(screen, buttons):

    font = pygame.font.Font(None, 36)
    player_label = font.render("Player:", True, (255, 255, 255))
    if buttons:
        label_rect = player_label.get_rect(midbottom=(buttons[0]["rect"].centerx, buttons[0]["rect"].top - 10))
        screen.blit(player_label, label_rect)

    color = (0,0,255)

    for btn in buttons:
        draw_button(screen, btn["text"], btn["rect"], color)


def draw_button(screen, text, rect, color, text_color=(255, 255, 255)):
    font = pygame.font.Font(None, 36)
    
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))

def draw_algorithm_buttons(screen, buttons, selected_text=None):

    font = pygame.font.Font(None, 36)
    pc_label = font.render("PC:", True, (255, 255, 255))
    if buttons:
        label_rect = pc_label.get_rect(midbottom=(buttons[0]["rect"].centerx, buttons[0]["rect"].top - 10))
        screen.blit(pc_label, label_rect)

    for btn in buttons:
        is_selected = btn["text"] == selected_text
        is_cancel = btn["text"] == "Cancel Selection"
        if is_cancel:
            color = (190, 45, 45)
        else:
            color = (0, 180, 255) if is_selected else (0, 0, 255)

        pygame.draw.rect(screen, color, btn["rect"], border_radius=8)

        if is_selected:
            outline_rect = btn["rect"].inflate(8, 8)
            pygame.draw.rect(screen, (255, 215, 0), outline_rect, width=3, border_radius=10)

        label = font.render(btn["text"], True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=btn["rect"].center))

def draw_input_buttons(screen, input, algorithm):
    if algorithm not in ("Depth Limited Search", "Iterative Deepening"):
        return
    font = pygame.font.Font(None, 36)
    
    if algorithm == "Depth Limited Search":
        label_text = "Depth Limit"
    elif algorithm == "Iterative Deepening":
        label_text = "Max Depth"

    label = font.render(f"{label_text}: {input} (up and down arrows to change)", True, (255, 255, 255))
    rect = label.get_rect(center=(screen.get_width() // 2, screen.get_height() - 60))
    screen.blit(label, rect)

def draw_exit_button(screen, button):
    draw_button(screen, button["text"], button["rect"], (175, 35, 35))


def draw_game_menu_button(screen, button):
    draw_button(screen, button["text"], button["rect"], (40, 120, 210))


def draw_completion_screen(screen, moves, buttons, level=None):
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 165))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 72)
    text_font = pygame.font.Font(None, 44)

    title = title_font.render("Level Complete!", True, (255, 255, 255))
    score = text_font.render(f"Moves: {moves}", True, (255, 215, 120))

    if level is not None:
        subtitle = text_font.render(f"Level {level}", True, (220, 220, 220))
        subtitle_rect = subtitle.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 10))
        screen.blit(subtitle, subtitle_rect)

    title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 80))
    score_rect = score.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))

    screen.blit(title, title_rect)
    screen.blit(score, score_rect)

    draw_button(screen, buttons["menu"]["text"], buttons["menu"]["rect"], (40, 120, 210))
    draw_button(screen, buttons["retry"]["text"], buttons["retry"]["rect"], (0, 140, 90))

