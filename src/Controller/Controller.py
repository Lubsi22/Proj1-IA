## @file Controller.py
#  @brief Game controller for the Water Sort puzzle.
#
#  Handles bottle selection, pouring logic, win detection,
#  and state generation for the search algorithms.
 
import copy

from Model.Bottle import Bottle

## @brief Tracks the currently selected bottle for the player's two-click interaction.
#
#  Set to a Bottle instance when the player clicks a source bottle,
#  and reset to None after a move is made, cancelled, or rejected.

selected_bottle = None

## @brief Returns the currently selected bottle.
#  @return The selected Bottle instance, or None if no bottle is selected.
def get_selected_bottle():
    return selected_bottle

## @brief Clears the current bottle selection.
#
#  Called when resetting the game state or launching a new level
#  to ensure no stale selection carries over.
def clear_selected_bottle():
    global selected_bottle
    selected_bottle = None

## @brief Calculates how many color units can be poured from source into destination.
#
#  A pour is only valid if:
#  - The source is non-empty.
#  - The destination is not full.
#  - The destination is either empty or its top color matches the source's top color.
#
#  The amount poured is the minimum of the consecutive same-color stack on top
#  of the source and the free slots available in the destination.
#
#  @param source      The Bottle to pour from.
#  @param destination The Bottle to pour into.
#  @return The number of color units that can be poured (0 if the move is invalid).
def _pour_amount(source, destination):
    
    if not source.colors or len(destination.colors) >= destination.capacity:
        return 0

    origin_color = source.colors[-1]

    if destination.colors and destination.colors[-1] != origin_color:
        return 0

    available_same_color = 0
    for color in reversed(source.colors):
        if color == origin_color:
            available_same_color += 1
        else:
            break

    free_slots = destination.capacity - len(destination.colors)
    return min(available_same_color, free_slots)


## @brief Handles a mouse click on the bottle grid for the player interaction.
#
#  Implements the two-click selection model:
#  - First click selects a source bottle.
#  - Second click on the same bottle deselects it.
#  - Second click on a different bottle attempts a move.
#
#  @param mouse_pos A tuple (x, y) representing the mouse click position.
#  @param bottles   The list of Bottle objects in the current level.
#  @return A dict describing the outcome, with a "type" key that is one of:
#          - "selected"   – a source bottle was chosen.
#          - "deselected" – the selected bottle was clicked again.
#          - "move"       – a valid pour was identified; includes "source",
#                           "destination", "color", and "amount" keys.
#          - "invalid"    – the destination click was not a legal move.
#          - None         – the click did not land on any bottle.
def select_bottle(mouse_pos, bottles):
    global selected_bottle

    for bottle in bottles:
        if (
                bottle.x <= mouse_pos[0] <= bottle.x + bottle.width
                and bottle.y <= mouse_pos[1] <= bottle.y + bottle.height
        ):
            if bottle == selected_bottle:
                selected_bottle = None
                print("Deselecting bottle")
                return {"type": "deselected"}
            if selected_bottle is None:
                selected_bottle = bottle
                print("Selected source")
                return {"type": "selected", "source": bottle}
            else:
                print("Selected destination")
                source = selected_bottle
                move_amount = _pour_amount(source, bottle)
                if move_amount > 0:
                    selected_bottle = None
                    return {
                        "type": "move",
                        "source": source,
                        "destination": bottle,
                        "color": source.colors[-1],
                        "amount": move_amount,
                    }
                else:
                    selected_bottle = None
                    print("Invalid move")
                    return {"type": "invalid"}

            break

    return None

## @brief Executes a pour from source into destination, mutating both bottles in place.
#
#  Pours as many consecutive same-color units from the top of source as will
#  fit in destination. The pour stops early if the destination fills up or
#  the next color in source differs from the poured color.
#
#  @param source      The Bottle to pour from.
#  @param destination The Bottle to pour into.
#  @return True if at least one unit was poured, False if the move is invalid.
def pour(source, destination):

    if source.colors and len(destination.colors) < destination.capacity:
        originColor = source.colors[-1]

        if destination.colors and destination.colors[-1] != originColor:
            return False

        source.colors.pop()
        destination.colors.append(originColor)
        currColor = originColor
        while(len(destination.colors) < destination.capacity and originColor == currColor and source.colors):
            if(source.colors[-1] == originColor):
                currColor = source.colors.pop()
                destination.colors.append(currColor)
            else:
                break


        return True

    return False

## @brief Checks whether the current bottle state satisfies the win condition.
#
#  The puzzle is solved when every bottle is either empty or completely filled
#  with a single uniform color.
#
#  @param bottles The list of Bottle objects to evaluate.
#  @return True if all bottles pass their color check, False otherwise.
def check_win(bottles):

    if not bottles:
        return False

    for bottle in bottles:
        if not bottle.check_color():
            return False

    return True

## @brief Creates a deep copy of a list of bottles.
#
#  Used by the search algorithms to generate independent successor states
#  without mutating the original bottle list.
#
#  @param bottles The list of Bottle objects to copy.
#  @return A new list of Bottle objects with the same colors, coordinates,
#          capacity, and visual capacity as the originals.
def copy_bottles(bottles):
    new_bottles = []
    for b in bottles:
        new_b = Bottle(list(b.colors), b.cords, b.capacity, b.visual_capacity)
        new_bottles.append(new_b)
    return new_bottles


## @brief Generates all valid successor states from the current bottle configuration.
#
#  For every ordered pair of distinct bottles (i, j), attempts a pour from i
#  into j on a copy of the state. If the pour succeeds, the resulting state is
#  added to the list of successors.
#
#  This function is passed as the operators callable to the search algorithms.
#
#  @param bottles The current list of Bottle objects (not mutated).
#  @return A list of bottle lists, each representing a reachable successor state.
def child_bottle_states(bottles):
    new_states = []
    for i in bottles:
        for j in bottles:
            if i != j:
                bottles_copy = copy_bottles(bottles)
                src = bottles_copy[bottles.index(i)]
                dst = bottles_copy[bottles.index(j)]
                if pour(src, dst):
                    new_states.append(bottles_copy)
    return new_states