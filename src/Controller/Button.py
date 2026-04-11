import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

LEVEL_BUTTON_WIDTH = 220
ALGORITHM_BUTTON_WIDTH = 300
EXIT_BUTTON_WIDTH = 200
GAME_MENU_BUTTON_WIDTH = 180
COMPLETE_BUTTON_WIDTH = 220
BUTTON_HEIGHT = 40
ROW_GAP = 12
COLUMN_GAP = 80


def _column_start_y(rows):
    total_height = rows * BUTTON_HEIGHT + (rows - 1) * ROW_GAP
    return (SCREEN_HEIGHT - total_height) // 2


def _column_x_positions():
    total_width = LEVEL_BUTTON_WIDTH + COLUMN_GAP + ALGORITHM_BUTTON_WIDTH
    left_x = (SCREEN_WIDTH - total_width) // 2
    right_x = left_x + LEVEL_BUTTON_WIDTH + COLUMN_GAP
    return left_x, right_x

def level_buttons(num_levels):
    left_x, _ = _column_x_positions()
    start_y = _column_start_y(num_levels)
    buttons = [
        {
            "text": f"Level {i+1}",
            "level": i + 1,
            "rect": pygame.Rect(
                left_x,
                start_y + i * (BUTTON_HEIGHT + ROW_GAP),
                LEVEL_BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
        }
        for i in range(num_levels)
    ]
    return buttons

def algorithm_buttons():
    _, right_x = _column_x_positions()
    labels = [
        "Breadth First Search",
        "Depth First Search",
        "Depth Limited Search",
        "Iterative Deepening",
        "A* Search",
        "Cancel Selection",
    ]
    start_y = _column_start_y(len(labels))
    buttons = [
        {
            "text": label,
            "rect": pygame.Rect(
                right_x,
                start_y + i * (BUTTON_HEIGHT + ROW_GAP),
                ALGORITHM_BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
        }
        for i, label in enumerate(labels)
    ]
    return buttons


def exit_button(num_levels):
    level_end_y = _column_start_y(num_levels) + num_levels * BUTTON_HEIGHT + (num_levels - 1) * ROW_GAP
    algorithm_rows = 6
    algorithm_end_y = _column_start_y(algorithm_rows) + algorithm_rows * BUTTON_HEIGHT + (algorithm_rows - 1) * ROW_GAP
    button_y = max(level_end_y, algorithm_end_y) + 36
    button_x = (SCREEN_WIDTH - EXIT_BUTTON_WIDTH) // 2

    return {
        "text": "Exit",
        "rect": pygame.Rect(button_x, button_y, EXIT_BUTTON_WIDTH, BUTTON_HEIGHT),
    }


def game_menu_button():
    return {
        "text": "Main Menu",
        "rect": pygame.Rect(20, 20, GAME_MENU_BUTTON_WIDTH, BUTTON_HEIGHT),
    }


def completion_buttons():
    gap = 30
    total_width = COMPLETE_BUTTON_WIDTH * 2 + gap
    start_x = (SCREEN_WIDTH - total_width) // 2
    y = (SCREEN_HEIGHT // 2) + 70

    return {
        "menu": {
            "text": "Main Menu",
            "rect": pygame.Rect(start_x, y, COMPLETE_BUTTON_WIDTH, BUTTON_HEIGHT),
        },
        "retry": {
            "text": "Retry Level",
            "rect": pygame.Rect(start_x + COMPLETE_BUTTON_WIDTH + gap, y, COMPLETE_BUTTON_WIDTH, BUTTON_HEIGHT),
        },
    }

