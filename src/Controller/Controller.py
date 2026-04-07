import copy

from Model.Bottle import Bottle
selected_bottle = None

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
                continue
            if selected_bottle is None:
                selected_bottle = bottle
                print("Selected source")
            else:
                print("Selected destination")
                if pour(selected_bottle, bottle):
                    selected_bottle = None
                else:
                    selected_bottle = None
                    print("Invalid move")

            break


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
        new_b = Bottle(list(b.colors), b.cords, b.capacity)
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