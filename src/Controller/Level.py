from Model.Bottle import Bottle

def level1():
    bottle1 = Bottle(['red', 'red', 'blue'], [(60, 60), (60, 140), (140, 140), (140, 60)])
    bottle2 = Bottle(['red', 'blue', 'blue'], [(160, 60), (160, 140), (240, 140), (240, 60)])
    bottle3 = Bottle([], [(260, 60), (260, 140), (340, 140), (340, 60)])
    return [bottle1, bottle2, bottle3]

level_loader = {
    1: level1,
    
}