import pygame
import time

from Controller.Controller import select_bottle, check_win
from Controller.Level import level_loader
from View.Draw import draw_level, draw_level_buttons, draw_algorithm_buttons
from Controller.Button import level_buttons, algorithm_buttons
from Search.File import print_to_file
from Search.Algorithms import a_star_search, breadth_first_search, depth_first_search, check_win, child_bottle_states


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

MENU = "menu"
LEVEL = "level"
PC = "pc"

def reset_menu():
    return {
        "state": MENU,
        "bottles": None,
        "current_level": None,
        "level_buttons": level_buttons(num_levels),
        "algorithm_buttons": algorithm_buttons(),
        "pc_moves": [],
        "pc_move_index": 0,
        "pc_last_time": 0,
        "pc_algorithm": None,
        
    }

num_levels = 1
g = reset_menu()

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and g["state"] == MENU:
            for a_btn in g["algorithm_buttons"]:
                if a_btn["rect"].collidepoint(event.pos):
                    g["pc_algorithm"] = a_btn["text"]
 
            for btn in g["level_buttons"]:
                if btn["rect"].collidepoint(event.pos):
                    g["current_level"] = btn["level"]
                    bottles = level_loader[btn["level"]]()
                    if g["pc_algorithm"]:
                        if g["pc_algorithm"] == "Breadth First Search":
                            goal = breadth_first_search(bottles, check_win, child_bottle_states)
                        elif g["pc_algorithm"] == "Depth First Search":
                            goal = depth_first_search(bottles, check_win, child_bottle_states)
                        else:
                            goal = a_star_search(bottles, check_win, child_bottle_states)

                        print_to_file(g["pc_algorithm"], num_levels)

                        path = []
                        node = goal
                        while node:
                            path.append(node.state)
                            node = node.parent
                        path.reverse()

                        g["pc_moves"] = path
                        g["pc_move_index"] = 0
                        g["pc_last_time"] = time.time()
                        g["bottles"] = path[0] if path else bottles
                        g["state"] = PC

                    else:
                        g["bottles"] = bottles
                        g["state"] = LEVEL
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and g["state"] == LEVEL:
            select_bottle(pygame.mouse.get_pos(), bottles)

        
    if g["state"] == PC:
        now = time.time()
        if now - g["pc_last_time"] >= 1.0:
            g["pc_move_index"] += 1
            g["pc_last_time"] = now
            if g["pc_move_index"] < len(g["pc_moves"]):
                g["bottles"] = g["pc_moves"][g["pc_move_index"]]
            else:
                g = reset_menu()

    if g["state"] == LEVEL and check_win(g["bottles"]):
        g = reset_menu()
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    if g["state"] == MENU:
        draw_level_buttons(screen, g["level_buttons"])
        draw_algorithm_buttons(screen, g["algorithm_buttons"])
    elif g["state"] in (LEVEL, PC):
        draw_level(screen, g["bottles"])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

