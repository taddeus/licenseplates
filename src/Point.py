class Point:
    def __init__(self, corner = None, coordinates = None):
        if corner != None:
            self.x = corner.getAttribute("x")
            self.y = corner.getAttribute("y")
        elif coordinates != None:
            self.x = coordinates[0]
            self.y = coordinates[1]
