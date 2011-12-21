from os import mkdir
from os.path import exists
from pylab import imsave, array, zeros, inv, dot, norm, svd, floor
from xml.dom.minidom import parse
from Character import Character
from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from LicensePlate import LicensePlate

# Gets the character data from a picture with a license plate
def retrieve_data(plate, corners):
    x0,y0, x1,y1, x2,y2, x3,y3 = corners

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

    P = get_transformation_matrix(matrix)
    data = array([zeros(M, float)] * N)

    for i in range(M):
        for j in range(N):
            or_coor   = dot(P, ([[i],[j],[1]]))
            or_coor_h = (or_coor[1][0] / or_coor[2][0],
                         or_coor[0][0] / or_coor[2][0])

            data[j][i] = pV(plate, or_coor_h[0], or_coor_h[1])

    return data

def get_transformation_matrix(matrix):
    # Get the vector p and the values that are in there by taking the SVD.
    # Since D is diagonal with the eigenvalues sorted from large to small
    # on the diagonal, the optimal q in min ||Dq|| is q = [[0]..[1]].
    # Therefore, p = Vq means p is the last column in V.
    U, D, V = svd(matrix)
    p = V[8][:]

    return inv(array([[p[0],p[1],p[2]], [p[3],p[4],p[5]], [p[6],p[7],p[8]]]))

def pV(image, x, y):
    #Get the value of a point (interpolated x, y) in the given image
    if not image.in_bounds(x, y):
      return 0

    x_low, x_high = floor(x), floor(x+1)
    y_low, y_high = floor(y), floor(y+1)
    x_y    = (x_high - x_low) * (y_high - y_low)

    a = x_high - x
    b = y_high - y
    c = x - x_low
    d = y - y_low

    return image[x_low,  y_low] / x_y * a * b \
        + image[x_high,  y_low] / x_y * c * b \
        + image[x_low , y_high] / x_y * a * d \
        + image[x_high, y_high] / x_y * c * d

def xml_to_LicensePlate(filename, save_character=None):
    plate   = GrayscaleImage('../images/Images/%s.jpg' % filename)
    dom     = parse('../images/Infos/%s.info' % filename)
    country = ''
    result  = []
    version = get_node(dom, "current-version")
    infos   = by_tag(dom, "info")

    for info in infos:
        if not version == get_node(info, "version"):
            continue

        country = get_node(info, "identification-letters")
        temp    = by_tag(info, "characters")

        if not temp: # no characters where found in the file
            break

        characters = temp[0].childNodes

        for i, char in enumerate(characters):
            if not char.nodeName == "character":
              continue

            value   = get_node(char, "char")
            corners = get_corners(char)

            if not len(corners) == 8:
                break

            data  = retrieve_data(plate, corners)
            image = NormalizedCharacterImage(data=data)
            result.append(Character(value, corners, image, filename))
        
            if save_character:
                character_image = GrayscaleImage(data=data)
                path       = "../images/LearningSet/%s" % value
                image_path = "%s/%d_%s.jpg" % (path, i, filename.split('/')[-1])

                if not exists(path):
                  mkdir(path)

                if not exists(image_path):
                  character_image.save(image_path)

    return LicensePlate(country, result)

def get_node(node, tag):
    return by_tag(node, tag)[0].firstChild.data

def by_tag(node, tag):
    return node.getElementsByTagName(tag)

def get_attr(node, attr):
  return int(node.getAttribute(attr))

def get_corners(dom):
    p = by_tag(dom, "point")

    # Extra padding
    y = 3
    x = 2

    # return 8 values (x0,y0, .., x3,y3)
    return get_attr(p[0], "x") - x, get_attr(p[0], "y") - y,\
           get_attr(p[1], "x") + x, get_attr(p[1], "y") - y,\
           get_attr(p[2], "x") + x, get_attr(p[2], "y") + y,\
           get_attr(p[3], "x") - x, get_attr(p[3], "y") + y