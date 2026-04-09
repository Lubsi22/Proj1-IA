import copy

from Model.Bottle import Bottle
selected_bottle = None


def get_selected_bottle():
    return selected_bottle


def clear_selected_bottle():
    global selected_bottle
    selected_bottle = None


def _pour_amount(source, destination):
    if not source.colors or len(destination.colors) >= destination.capacity:
        return 0

    origin_color = source.colors[-1]
    available_same_color = 0
    for color in reversed(source.colors):
        if color == origin_color:
            available_same_color += 1
        else:
            break

    free_slots = destination.capacity - len(destination.colors)
    return min(available_same_color, free_slots)


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


def pour(source, destination):

    if source.colors and len(destination.colors) < destination.capacity:
        originColor = source.colors[-1]

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


def check_win(bottles):

    if not bottles:
        return False

    for bottle in bottles:
        if not bottle.check_color():
            return False

    return True

def copy_bottles(bottles):
    new_bottles = []
    for b in bottles:
        new_b = Bottle(list(b.colors), b.cords, b.capacity, b.visual_capacity)
        new_bottles.append(new_b)
    return new_bottles

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