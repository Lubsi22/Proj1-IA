from Model.Bottle import Bottle

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTLE_WIDTH = 80
BOTTLE_GAP = 20
LAYER_HEIGHT = 22


def build_level(level_data):
    capacities = [capacity for _, capacity in level_data]
    max_capacity = max(capacities)
    bottle_height = max_capacity * LAYER_HEIGHT
    top_y = (SCREEN_HEIGHT - bottle_height) // 2
    bottle_count = len(level_data)
    total_width = bottle_count * BOTTLE_WIDTH + (bottle_count - 1) * BOTTLE_GAP
    start_x = (SCREEN_WIDTH - total_width) // 2

    bottles = []
    for idx, (colors, capacity) in enumerate(level_data):
        x = start_x + idx * (BOTTLE_WIDTH + BOTTLE_GAP)
        cords = [
            (x, top_y),
            (x, top_y + bottle_height),
            (x + BOTTLE_WIDTH, top_y + bottle_height),
            (x + BOTTLE_WIDTH, top_y),
        ]
        bottles.append(Bottle(list(colors), cords, capacity, visual_capacity=max_capacity))

    return bottles


def level1():
    data = [
        (['red', 'red', 'blue'], 3),
        (['red', 'blue', 'blue'], 3),
        ([], 3),
    ]
    return build_level(data)


def level2():
    data = [
        (['red', 'green', 'blue'], 3),
        (['blue', 'red', 'green'], 3),
        (['green', 'blue', 'red'], 3),
        ([], 4),
    ]
    return build_level(data)


def level3():
    data = [
        (['yellow', 'red', 'blue', 'green'], 4),
        (['green', 'yellow', 'red', 'blue'], 4),
        (['blue', 'green', 'yellow', 'red'], 4),
        (['red', 'blue', 'green', 'yellow'], 4),
        ([], 4),
        ([], 4),
    ]
    return build_level(data)


def level4():
    data = [
        (['purple', 'orange', 'purple', 'orange'], 4),
        (['cyan', 'purple', 'cyan', 'purple'], 4),
        (['orange', 'cyan', 'orange', 'cyan'], 4),
        ([], 4),
        ([], 4),
    ]
    return build_level(data)


def level5():
    data = [
        (['pink', 'teal', 'lime', 'pink'], 5),
        (['lime', 'pink', 'teal', 'brown'], 5),
        (['teal', 'brown', 'pink', 'lime'], 5),
        (['brown', 'lime', 'brown', 'teal'], 5),
        (['teal', 'pink', 'lime', 'brown'], 5),
        ([], 5),
        ([], 5),
    ]
    return build_level(data)


def level6():
    data = [
        (['red', 'blue', 'green', 'yellow'], 4),
        (['yellow', 'purple', 'red', 'orange'], 4),
        (['orange', 'green', 'purple', 'blue'], 4),
        (['blue', 'yellow', 'orange', 'green'], 4),
        (['green', 'red', 'yellow', 'purple'], 4),
        (['purple', 'orange', 'blue', 'red'], 4),
        ([], 4),
        ([], 4),
    ]
    return build_level(data)


level_loader = {
    1: level1,
    2: level2,
    3: level3,
    4: level4,
    5: level5,
    6: level6,
}
