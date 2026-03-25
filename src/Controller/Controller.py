import pygame

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
                    print("Invalid move")

            break


def pour(source, destination):

    if source.colors and len(destination.colors) < 3:
        originColor = source.colors.pop()
        destination.colors.append(originColor)
        currColor = originColor
        while(len(destination.colors) < 3 and originColor == currColor and source.colors):
            if(source.colors[-1] == originColor):
                currColor = source.colors.pop()
                destination.colors.append(currColor)
            else:
                break


        return True

    return False


def check_win(bottles):

    for bottle in bottles:
        if not bottle.check_color():
            return False

    return True

