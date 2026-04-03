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

def algorithm_buttons():

    button_width, button_height = 300, 40 
    buttons = [
        {
            "text": "Breadth First Search",
            "rect": pygame.Rect(400, 50 + 0 * 50, button_width, button_height),
        },
        {
            "text": "Depth First Search",
            "rect": pygame.Rect(400, 50 + 1 * 50, button_width, button_height),
        },
        {
            "text": "A* Search",
            "rect": pygame.Rect(400, 50 + 2 * 50, button_width, button_height)
        }

    ]
    return buttons

