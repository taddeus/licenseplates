from os import mkdir
from os.path import exists
from math import acos
from pylab import imsave, array, zeros, inv, dot, norm, svd, floor
from xml.dom.minidom import parse
from Point import Point
from GrayscaleImage import GrayscaleImage

class LearningSetGenerator:

    def __init__(self, folder_nr, file_nr):
        filename = '%04d/00991_%04d%02d' % (folder_nr, folder_nr, file_nr)

        self.image = GrayscaleImage('../images/Images/%s.jpg' % filename)
        self.read_xml(filename)

    # sets the entire license plate of an image
    def retrieve_data(self, corners):
        x0, y0 = corners[0].to_tuple()
        x1, y1 = corners[1].to_tuple()
        x2, y2 = corners[2].to_tuple()
        x3, y3 = corners[3].to_tuple()

        M = int(1.2 * (max(x0, x1, x2, x3) - min(x0, x1, x2, x3)))
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

    def read_xml(self, filename):
        dom = parse('../images/Infos/%s.info' % filename)
        self.characters = []

        version = dom.getElementsByTagName("current-version")[0].firstChild.data
        info    = dom.getElementsByTagName("info")

        for i in info:
            if version == i.getElementsByTagName("version")[0].firstChild.data:

                self.country = i.getElementsByTagName("identification-letters")[0].firstChild.data
                temp = i.getElementsByTagName("characters")

                if len(temp):
                  characters = temp[0].childNodes
                else:
                  self.characters = []
                  break

                for i, character in enumerate(characters):
                    if character.nodeName == "character":
                        value   = character.getElementsByTagName("char")[0].firstChild.data
                        corners = self.get_corners(character)

                        if not len(corners) == 4:
                          break

                        image = GrayscaleImage(data = self.retrieve_data(corners))

                        print value

                        path = "../images/LearningSet/%s" % value
                        image_path = "%s/%d_%s.jpg" % (path, i, filename.split('/')[-1])

                        if not exists(path):
                          mkdir(path)

                        if not exists(image_path):
                          image.save(image_path)

                break

    def get_corners(self, dom):
      nodes = dom.getElementsByTagName("point")

      corners = []

      for node in nodes:
          corners.append(Point(node))

      return corners


for i in range(9):
    for j in range(100):
        try:
            filename = '%04d/00991_%04d%02d.info' % (i, i, j)
            print 'loading file "%s"' % filename
            plate = LearningSetGenerator(i, j)
        except:
            print "failure"
