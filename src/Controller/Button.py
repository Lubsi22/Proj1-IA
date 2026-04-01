import pygame

def level_buttons(num_levels):
    button_width, button_height = 150, 40
    buttons = [
        {
            "text": f"Level {i+1}",
            "level": i + 1,
            "rect": pygame.Rect(100, 50 + i * 50, button_width, button_height),
        }
        for i in range(num_levels)
    ]
    return buttons
