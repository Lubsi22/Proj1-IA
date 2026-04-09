
class Bottle:

    def __init__(self, colors, cords, capacity, visual_capacity=None):
        self.colors = colors
        self.cords = cords
        self.capacity = capacity
        self.visual_capacity = visual_capacity if visual_capacity is not None else capacity

        self.x = cords[0][0]
        self.y = cords[0][1]
        self.width = cords[3][0] - cords[0][0]
        self.height = cords[1][1] - cords[0][1]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
        
    def __str__(self):
        return str(self.colors) #+ ", " + str(self.cords)

    def check_color(self):
        if len(self.colors) == 0:
            return True
        if len(self.colors) != self.capacity:
            return False
        color_bottle = self.colors[0]
        for color in self.colors[1:]:
            if color != color_bottle:
                return False

        return True