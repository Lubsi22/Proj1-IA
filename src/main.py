import pygame
import time
import os

from Controller.Controller import (
    select_bottle,
    pour,
    get_selected_bottle,
    clear_selected_bottle,
    check_win,
)
from Controller.Level import level_loader
from View.Draw import draw_level, draw_level_buttons, draw_algorithm_buttons, draw_input_buttons, draw_exit_button, draw_game_menu_button, draw_completion_screen, draw_move_counter, draw_button, draw_hint_button
from Controller.Button import level_buttons, algorithm_buttons, exit_button, run_all_button, game_menu_button, completion_buttons, hint_button
from Search.File import print_to_file, run_all_algorithms_from_file
from Search.Algorithms import a_star_search, breadth_first_search, depth_first_search, depth_limited_search, iterative_deepening_search, uniform_cost_search, check_win, child_bottle_states, greedy_search, weighted_astar_search


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

MENU = "menu"
LEVEL = "level"
PC = "pc"
COMPLETE = "complete"

def compute_hint(bottles):
    goal = a_star_search(bottles, check_win, child_bottle_states)
    if goal is None:
        return None, None
 
    path = []
    node = goal
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
 
    if len(path) < 2:
        return None, None
 
    current_state = path[0]
    next_state    = path[1]
 
    src_idx = dst_idx = None
    for i, (cur, nxt) in enumerate(zip(current_state, next_state)):
        if len(cur.colors) > len(nxt.colors):
            src_idx = i
        elif len(cur.colors) < len(nxt.colors):
            dst_idx = i
 
    return src_idx, dst_idx


def open_completion(game, moves):
    clear_selected_bottle()
    game["move_count"] = moves
    game["state"] = COMPLETE


def launch_level(game, level):
    game["current_level"] = level
    bottles = level_loader[level]()
    clear_selected_bottle()

    if game["pc_algorithm"]:
        if game["pc_algorithm"] == "Breadth First Search":
            goal = breadth_first_search(bottles, check_win, child_bottle_states)
        elif game["pc_algorithm"] == "Depth First Search":
            goal = depth_first_search(bottles, check_win, child_bottle_states)
        elif game["pc_algorithm"] == "Depth Limited Search":
            goal = depth_limited_search(bottles, check_win, child_bottle_states, game["depth_limit"])
        elif game["pc_algorithm"] == "Iterative Deepening":
            goal = iterative_deepening_search(bottles, check_win, child_bottle_states, game["max_depth"])
        elif game["pc_algorithm"] == "Uniform Cost":
            goal = uniform_cost_search(bottles, check_win, child_bottle_states)
        elif game["pc_algorithm"] == "Greedy Search":
            goal = greedy_search(bottles, check_win, child_bottle_states)
        elif game["pc_algorithm"] == "Weighted A*":
            goal = weighted_astar_search(bottles, check_win, child_bottle_states, game["weight"])
        else:
            goal = a_star_search(bottles, check_win, child_bottle_states)

        if goal is None:
            game["state"] = MENU
            return

        print_to_file(game["pc_algorithm"], game["current_level"], game["depth_limit"], game["max_depth"], game["weight"])

        path = []
        node = goal
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()

        game["pc_moves"] = path
        game["pc_move_index"] = 0
        game["pc_last_time"] = time.time()
        game["move_count"] = 0
        game["bottles"] = path[0] if path else bottles
        game["state"] = PC
    else:
        game["pc_moves"] = []
        game["pc_move_index"] = 0
        game["move_count"] = 0
        game["bottles"] = bottles
        game["state"] = LEVEL

def reset_menu():
    clear_selected_bottle()
    return {
        "state": MENU,
        "bottles": None,
        "current_level": None,
        "level_buttons": level_buttons(num_levels),
        "algorithm_buttons": algorithm_buttons(),
        "depth_limit": 10,
        "max_depth": 30,
        "weight": 1.5,
        "exit_button": exit_button(num_levels),
        "run_all_button": run_all_button(),
        "game_menu_button": game_menu_button(),
        "hint_button": hint_button(),
        "completion_buttons": completion_buttons(),
        "pc_moves": [],
        "pc_move_index": 0,
        "pc_last_time": 0,
        "pc_algorithm": None,
        "move_count": 0,
        "hint_src_idx": None,
        "hint_dst_idx": None,
        
    }

num_levels = len(level_loader)
g = reset_menu()

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and g["state"] == MENU:
            if g["exit_button"]["rect"].collidepoint(event.pos):
                running = False
                break
            if g["run_all_button"]["rect"].collidepoint(event.pos):
                input_file = os.path.join(os.path.dirname(__file__), "Search", "levels.txt")
                run_all_algorithms_from_file(input_file)

            for a_btn in g["algorithm_buttons"]:
                if a_btn["rect"].collidepoint(event.pos):
                    if a_btn["text"] == "Cancel Selection":
                        g["pc_algorithm"] = None
                    else:
                        g["pc_algorithm"] = a_btn["text"]
 
            for btn in g["level_buttons"]:
                if btn["rect"].collidepoint(event.pos):
                    launch_level(g, btn["level"])
                    break
        
        elif event.type == pygame.KEYDOWN and g["state"] == MENU:
            if g["pc_algorithm"] == "Depth Limited Search":
                if event.key == pygame.K_UP:
                    g["depth_limit"] = min(50, g["depth_limit"] + 1)
                elif event.key == pygame.K_DOWN:
                    g["depth_limit"] = max(1, g["depth_limit"] - 1)

            elif g["pc_algorithm"] == "Iterative Deepening":
                if event.key == pygame.K_UP:
                    g["max_depth"] = min(50, g["max_depth"] + 1)
                elif event.key == pygame.K_DOWN:
                    g["max_depth"] = max(1, g["max_depth"] - 1)

            elif g["pc_algorithm"] == "Weighted A*":
                if event.key == pygame.K_UP:
                    g["weight"] = min(50.5, g["weight"] + 0.5)
                elif event.key == pygame.K_DOWN:
                    g["weight"] = max(0.5, g["weight"] - 0.5)

        elif event.type == pygame.MOUSEBUTTONDOWN and g["state"] == COMPLETE:
            if g["completion_buttons"]["menu"]["rect"].collidepoint(event.pos):
                g = reset_menu()
                continue
            if g["completion_buttons"]["retry"]["rect"].collidepoint(event.pos) and g["current_level"]:
                launch_level(g, g["current_level"])
                continue
        elif event.type == pygame.MOUSEBUTTONDOWN and g["state"] in (LEVEL, PC):
            if g["game_menu_button"]["rect"].collidepoint(event.pos):
                g = reset_menu()
                continue

            if g["state"] == LEVEL:
                if g["hint_button"]["rect"].collidepoint(event.pos):
                    src, dst = compute_hint(g["bottles"])
                    g["hint_src_idx"] = src
                    g["hint_dst_idx"] = dst
                    continue

                move_result = select_bottle(event.pos, g["bottles"])
                if move_result and move_result.get("type") == "move":
                    if pour(move_result["source"], move_result["destination"]):
                        g["move_count"] += 1
                        g["hint_src_idx"] = None
                        g["hint_dst_idx"] = None

        
    if g["state"] == PC:
        now = time.time()
        if now - g["pc_last_time"] >= 1.0:
            g["pc_move_index"] += 1
            g["pc_last_time"] = now
            if g["pc_move_index"] < len(g["pc_moves"]):
                g["bottles"] = g["pc_moves"][g["pc_move_index"]]
            else:
                open_completion(g, max(0, len(g["pc_moves"]) - 1))

    if g["state"] == LEVEL and check_win(g["bottles"]):
        open_completion(g, g["move_count"])
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    if g["state"] == MENU:
        draw_level_buttons(screen, g["level_buttons"])
        draw_algorithm_buttons(screen, g["algorithm_buttons"], g["pc_algorithm"])
        draw_exit_button(screen, g["exit_button"])
        draw_button(screen, g["run_all_button"]["text"], g["run_all_button"]["rect"], (0, 150, 100))

        if g["pc_algorithm"] == "Depth Limited Search":
            draw_input_buttons(screen, g["depth_limit"], g["pc_algorithm"])
        elif g["pc_algorithm"] == "Iterative Deepening":
            draw_input_buttons(screen, g["max_depth"], g["pc_algorithm"])
        elif g["pc_algorithm"] == "Weighted A*":
            draw_input_buttons(screen, g["weight"], g["pc_algorithm"])
    elif g["state"] in (LEVEL, PC):
        draw_level(
            screen,
            g["bottles"],
            selected_bottle=get_selected_bottle() if g["state"] == LEVEL else None,
            hint_src_idx=g.get("hint_src_idx") if g["state"] == LEVEL else None,
            hint_dst_idx=g.get("hint_dst_idx") if g["state"] == LEVEL else None,
        )
        draw_game_menu_button(screen, g["game_menu_button"])
        if g["state"] == LEVEL:
            draw_hint_button(screen, g["hint_button"])
            draw_move_counter(screen, g["move_count"])
        elif g["state"] == PC:
            total_moves = max(0, len(g["pc_moves"]) - 1)
            draw_move_counter(screen, g["pc_move_index"], total_moves)
    elif g["state"] == COMPLETE:
        draw_completion_screen(screen, g["move_count"], g["completion_buttons"], g["current_level"])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

