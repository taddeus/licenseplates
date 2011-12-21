from os import mkdir
from os.path import exists
from pylab import array, zeros, inv, dot, svd, floor
from xml.dom.minidom import parse
from Point import Point
from Character import Character
from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from LicensePlate import LicensePlate

# sets the entire license plate of an image
def retrieve_data(image, corners):
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

    P = inv(get_transformation_matrix(matrix))
    data = array([zeros(M, float)] * N)

    for i in range(M):
        for j in range(N):
            or_coor   = dot(P, ([[i],[j],[1]]))
            or_coor_h = (or_coor[1][0] / or_coor[2][0],
                         or_coor[0][0] / or_coor[2][0])

            data[j][i] = pV(image, or_coor_h[0], or_coor_h[1])

    return data

def get_transformation_matrix(matrix):
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

def pV(image, x, y):
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

def xml_to_LicensePlate(filename, save_character=None):
    image = GrayscaleImage('../images/Images/%s.jpg' % filename)
    dom   = parse('../images/Infos/%s.info' % filename)
    result_characters = []

    version = dom.getElementsByTagName("current-version")[0].firstChild.data
    info    = dom.getElementsByTagName("info")

    for i in info:
        if version == i.getElementsByTagName("version")[0].firstChild.data:

            country = i.getElementsByTagName("identification-letters")[0].firstChild.data
            temp = i.getElementsByTagName("characters")

            if len(temp):
              characters = temp[0].childNodes
            else:
              characters = []
              break

            for i, character in enumerate(characters):
                if character.nodeName == "character":
                    value   = character.getElementsByTagName("char")[0].firstChild.data
                    corners = get_corners(character)

                    if not len(corners) == 4:
                      break

                    character_data  = retrieve_data(image, corners)
                    character_image = NormalizedCharacterImage(data=character_data)

                    result_characters.append(Character(value, corners, character_image, filename))

                    if save_character:
                        single_character = GrayscaleImage(data=character_data)

                        path = "../images/LearningSet/%s" % value
                        image_path = "%s/%d_%s.jpg" % (path, i, filename.split('/')[-1])

                        if not exists(path):
                          mkdir(path)

                        if not exists(image_path):
                          single_character.save(image_path)

    return LicensePlate(country, result_characters)

def get_corners(dom):
    nodes = dom.getElementsByTagName("point")
    corners = []

    margin_y = 3
    margin_x = 2

    corners.append(
    Point(get_coord(nodes[0], "x") - margin_x,
          get_coord(nodes[0], "y") - margin_y)
    )

    corners.append(
    Point(get_coord(nodes[1], "x") + margin_x,
          get_coord(nodes[1], "y") - margin_y)
    )

    corners.append(
    Point(get_coord(nodes[2], "x") + margin_x,
          get_coord(nodes[2], "y") + margin_y)
    )

    corners.append(
    Point(get_coord(nodes[3], "x") - margin_x,
          get_coord(nodes[3], "y") + margin_y)
    )

    return corners

def get_coord(node, attribute):
    return int(node.getAttribute(attribute))
