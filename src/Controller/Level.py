from Model.Bottle import Bottle

def level1():
    bottle1 = Bottle(['red', 'red', 'blue'], [(60, 60), (60, 140), (140, 140), (140, 60)], 3)
    bottle2 = Bottle(['red', 'blue', 'blue'], [(160, 60), (160, 140), (240, 140), (240, 60)], 3)
    bottle3 = Bottle([], [(260, 60), (260, 140), (340, 140), (340, 60)], 3)
    return [bottle1, bottle2, bottle3]


def level2():
    bottle1 = Bottle(['red', 'green', 'blue'], [(60, 60), (60, 140), (140, 140), (140, 60)], 3)
    bottle2 = Bottle(['blue', 'red', 'green'], [(160, 60), (160, 140), (240, 140), (240, 60)], 3)
    bottle3 = Bottle(['green', 'blue', 'red'], [(260, 60), (260, 140), (340, 140), (340, 60)], 3)
    bottle4 = Bottle([], [(360, 60), (360, 140), (440, 140), (440, 60)], 4)
    return [bottle1, bottle2, bottle3, bottle4]

def level3():
    bottle1 = Bottle(['yellow', 'red', 'blue', 'green'], [(60, 60), (60, 140), (140, 140), (140, 60)], 4)
    bottle2 = Bottle(['green', 'yellow', 'red', 'blue'], [(160, 60), (160, 140), (240, 140), (240, 60)], 4)
    bottle3 = Bottle(['blue', 'green', 'yellow', 'red'], [(260, 60), (260, 140), (340, 140), (340, 60)], 4)
    bottle4 = Bottle(['red', 'blue', 'green', 'yellow'], [(360, 60), (360, 140), (440, 140), (440, 60)], 4)
    bottle5 = Bottle([], [(460, 60), (460, 140), (540, 140), (540, 60)], 4)
    bottle6 = Bottle([], [(560, 60), (560, 140), (640, 140), (640, 60)], 4)
    return [bottle1, bottle2, bottle3, bottle4, bottle5, bottle6]

def level4():
    bottle1 = Bottle(['purple', 'orange', 'purple', 'orange'], [(60, 60), (60, 140), (140, 140), (140, 60)], 4)
    bottle2 = Bottle(['cyan', 'purple', 'cyan', 'purple'],    [(160, 60), (160, 140), (240, 140), (240, 60)], 4)
    bottle3 = Bottle(['orange', 'cyan', 'orange', 'cyan'],    [(260, 60), (260, 140), (340, 140), (340, 60)], 4)
    bottle4 = Bottle([], [(360, 60), (360, 140), (440, 140), (440, 60)], 4)
    bottle5 = Bottle([], [(460, 60), (460, 140), (540, 140), (540, 60)], 4)
    return [bottle1, bottle2, bottle3, bottle4, bottle5]

def level5():
    bottle1 = Bottle(['pink', 'teal', 'lime', 'pink'],   [(60, 60),  (60, 140),  (140, 140), (140, 60)], 5)
    bottle2 = Bottle(['lime', 'pink', 'teal', 'brown'],  [(160, 60), (160, 140), (240, 140), (240, 60)], 5)
    bottle3 = Bottle(['teal', 'brown', 'pink', 'lime'],  [(260, 60), (260, 140), (340, 140), (340, 60)], 5)
    bottle4 = Bottle(['brown', 'lime', 'brown', 'teal'], [(360, 60), (360, 140), (440, 140), (440, 60)], 5)
    bottle5 = Bottle(['teal', 'pink', 'lime', 'brown'],  [(460, 60), (460, 140), (540, 140), (540, 60)], 5)
    bottle6 = Bottle([], [(560, 60), (560, 140), (640, 140), (640, 60)], 5)
    bottle7 = Bottle([], [(660, 60), (660, 140), (740, 140), (740, 60)], 5)
    return [bottle1, bottle2, bottle3, bottle4, bottle5, bottle6, bottle7]

def level6():
    bottle1 = Bottle(['red', 'blue', 'green', 'yellow'],    [(60, 60),  (60, 140),  (140, 140), (140, 60)], 4)
    bottle2 = Bottle(['yellow', 'purple', 'red', 'orange'], [(160, 60), (160, 140), (240, 140), (240, 60)], 4)
    bottle3 = Bottle(['orange', 'green', 'purple', 'blue'],  [(260, 60), (260, 140), (340, 140), (340, 60)], 4)
    bottle4 = Bottle(['blue', 'yellow', 'orange', 'green'],  [(360, 60), (360, 140), (440, 140), (440, 60)], 4)
    bottle5 = Bottle(['green', 'red', 'yellow', 'purple'],   [(460, 60), (460, 140), (540, 140), (540, 60)], 4)
    bottle6 = Bottle(['purple', 'orange', 'blue', 'red'],    [(560, 60), (560, 140), (640, 140), (640, 60)], 4)
    bottle7 = Bottle([], [(660, 60), (660, 140), (740, 140), (740, 60)], 4)
    bottle8 = Bottle([], [(760, 60), (760, 140), (840, 140), (840, 60)], 4)
    return [bottle1, bottle2, bottle3, bottle4, bottle5, bottle6, bottle7, bottle8]

level_loader = {
    1: level1,
    2: level2,
    3: level3,
    4: level4,
    5: level5,
    6: level6,
}