from Point import Point

# TODO cleanup the getElements stuff
class Character:
    def __init__(self, character):
        self.dom     = character
        self.value   = self.get_node("char").firstChild.data

        self.set_corners()
        print self.corners

    def set_corners(self):
        corners = self.get_children("quadrangle")

        self.corners = []

        for corner in corners:
          if corner.nodeName == "point":
              self.corners.append(Point(corner))

    def get_node(self, node, dom=None):
        if not dom:
            dom = self.dom

        return dom.getElementsByTagName(node)[0]

    def get_children(self, node, dom=None):
        return self.get_node(node, dom).childNodes

    def get_feature_vector(self):
        pass
