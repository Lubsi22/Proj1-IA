import pygame

from Controller.Controller import select_bottle, check_win
from Controller.Level import level_loader
from View.Draw import draw_level, draw_level_buttons
from Controller.Button import level_buttons

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

MENU = "menu"
LEVEL = "level"

state = MENU
num_levels = 1
current_level = None
buttons = level_buttons(num_levels)
bottles = None

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and state == MENU:
            for btn in buttons:
                if btn["rect"].collidepoint(event.pos):
                    current_level = btn["level"]
                    bottles = level_loader[current_level]()
                    state = LEVEL
                    buttons = None
        elif event.type == pygame.MOUSEBUTTONDOWN and state == LEVEL:
            select_bottle(pygame.mouse.get_pos(), bottles)

    if check_win(bottles):
        running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    if state == MENU:
        draw_level_buttons(screen, buttons)
    elif state == LEVEL:
        draw_level(screen, bottles)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

