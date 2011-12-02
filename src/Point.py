class Point:
    def __init__(self, x_or_corner=None, y=None):
        if y != None:
            self.x = x_or_corner
            self.y = y
        else:
            self.x = int(x_or_corner.getAttribute("x"))
            self.y = int(x_or_corner.getAttribute("y"))

    def to_tuple(self):
        return self.x, self.y
        
    def __str__(self):
        return str(self.x) + " " + str(self.y)