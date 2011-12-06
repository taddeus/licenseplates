from pylab import array, zeros, inv, dot, svd, floor
from xml.dom.minidom import parse
from Point import Point
from Character import Character
from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage

class LicensePlate:

    def __init__(self, folder_nr, file_nr):
        filename = '%04d/00991_%04d%02d' % (folder_nr, folder_nr, file_nr)

        self.dom = parse('../images/Infos/%s.info' % filename)
        properties = self.get_properties()

        self.image = GrayscaleImage('../images/Images/%s.jpg' % filename)
        self.width = int(properties['width'])
        self.height = int(properties['height'])

        self.read_xml()

    def are_corners_sorted(corners):
        '''Check if points are sorted clockwise, starting in the left-top
        corner.'''
        x0, y0 = corners[0].to_tuple()
        x1, y1 = corners[1].to_tuple()
        x2, y2 = corners[2].to_tuple()
        x3, y3 = corners[3].to_tuple()

        return x0 < x1 and y1 <= y2 and x2 >= x3 and y3 > y0

    def sort_corners(corners):
        '''Sort the corners clockwise, starting in the left-top corner.'''
        tuples = []
        output = []

        for point in corners:
            tuples.append(point.to_tuple())

        bot1 = (0, 0)
        bot2 = (0, 0)
        top1 = None
        top2 = None

        # Get bottom points (where the y value is the largest). The top points
        # are the points that are not a bottom point.
        for tup in tuples:
            if tup[1] > bot1[1] or tup[1] > bot2[1]:
                if top1 == None:
                    top1 = bot2
                else:
                    top2 = bot2

                if tup[1] > bot1[1]:
                    bot2 = bot1
                    bot1 = tup
                else:
                    bot2 = tup
            else:
                if top1 == None:
                    top1 = tup
                else:
                    top2 = tup

        # First point is the smallest x-value top point, second is the other
        # top point
        if top1[0] < top2[0]:
            output.append(Point(top1[0], top1[1]))
            output.append(Point(top2[0], top2[1]))
        else:
            output.append(Point(top2[0], top2[1]))
            output.append(Point(top1[0], top1[1]))

        # Third point is the bottom point with the largest x-value, fourth is
        # the other bottom point
        if bot1[0] > bot2[0]:
            output.append(Point(bot1[0], bot1[1]))
            output.append(Point(bot2[0], bot2[1]))
        else:
            output.append(Point(bot2[0], bot2[1]))
            output.append(Point(bot1[0], bot1[1]))

        return output

    # sets the entire license plate of an image
    def retrieve_data(self, corners):
        x0, y0 = corners[0].to_tuple()
        x1, y1 = corners[1].to_tuple()
        x2, y2 = corners[2].to_tuple()
        x3, y3 = corners[3].to_tuple()

        M = max(x0, x1, x2, x3) - min(x0, x1, x2, x3)
        N = max(y0, y1, y2, y3) - min(y0, y1, y2, y3)

        matrix = array([
          [x0, y0, 1,  0,  0, 0,       0,       0,  0],
          [ 0,  0, 0, x0, y0, 1,       0,       0,  0],
          [x1, y1, 1,  0,  0, 0, -M * x0, -M * y1, -M],
          [ 0,  0, 0, x1, y1, 1,       0,       0,  0],
          [x2, y2, 1,  0,  0, 0, -M * x2, -M * y2, -M],
          [ 0,  0, 0, x2, y2, 1, -N * x2, -N * y2, -N],
          [x3, y3, 1,  0,  0, 0,       0,       0,  0],
          [ 0,  0, 0, x3, y3, 1, -N * x3, -N * y3, -N]
        ])

        P = inv(self.get_transformation_matrix(matrix))
        data = array([zeros(M, float)] * N)

        for i in range(0, M):
            for j in range(0, N):
                or_coor   = dot(P, ([[i],[j],[1]]))
                or_coor_h = (or_coor[1][0] / or_coor[2][0],
                             or_coor[0][0] / or_coor[2][0])

                data[j][i] = self.pV(or_coor_h[0], or_coor_h[1])

        return data

    def get_transformation_matrix(self, matrix):
        # Get the vector p and the values that are in there by taking the SVD.
        # Since D is diagonal with the eigenvalues sorted from large to small
        # on the diagonal, the optimal q in min ||Dq|| is q = [[0]..[1]].
        # Therefore, p = Vq means p is the last column in V.
        U, D, V = svd(matrix)
        p = V[8][:]

        return array([
            [ p[0], p[1], p[2] ],
            [ p[3], p[4], p[5] ],
            [ p[6], p[7], p[8] ]
        ])

    def pV(self, x, y):
        image = self.image

        #Get the value of a point (interpolated x, y) in the given image
        if image.in_bounds(x, y):
            x_low  = floor(x)
            x_high = floor(x + 1)
            y_low  = floor(y)
            y_high = floor(y + 1)
            x_y    = (x_high - x_low) * (y_high - y_low)

            a = x_high - x
            b = y_high - y
            c = x - x_low
            d = y - y_low

            return image[x_low,  y_low] / x_y * a * b \
                + image[x_high,  y_low] / x_y * c * b \
                + image[x_low , y_high] / x_y * a * d \
                + image[x_high, y_high] / x_y * c * d

        return 0

    # Testing purposes
    def show(self):
        from pylab import imshow, show
        imshow(self.data, cmap="gray")
        show()

    def get_properties(self):
        children = self.get_children("properties")

        properties = {}

        for child in children:
            if child.nodeType == child.TEXT_NODE:
                properties[child.nodeName] = child.data
            elif child.nodeType == child.ELEMENT_NODE:
                properties[child.nodeName] = child.firstChild.data

        return properties

    # TODO : create function for location / characters as they do the same
    def read_xml(self):
        children = self.get_children("plate") # most recent version

        for child in children:
            if child.nodeName == "regnum":
              self.license_full = child.firstChild.data
            elif child.nodeName == "identification-letters":
              self.country = child.firstChild.data
            elif child.nodeName == "location":
                self.corners = self.get_corners(child)
            elif child.nodeName == "characters":
                nodes = child.childNodes

                self.characters = []

                for character in nodes:
                  if character.nodeName == "character":
                    value   = self.get_node("char", character).firstChild.data
                    corners = self.get_corners(character)
                    data    = self.retrieve_data(corners)
                    image   = NormalizedCharacterImage(data=data)

                    self.characters.append(Character(value, corners, image))
            else:
                pass

    def get_node(self, node, dom=None):
        if not dom:
            dom = self.dom

        return dom.getElementsByTagName(node)[0]

    def get_children(self, node, dom=None):
        return self.get_node(node, dom).childNodes

    def get_corners(self, child):
      nodes = self.get_children("quadrangle", child)

      corners = []

      for corner in nodes:
        if corner.nodeName == "point":
            corners.append(Point(corner))

      return corners
