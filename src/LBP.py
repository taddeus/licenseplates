#!/usr/bin/python
import Image
from numpy import array, zeros, byte
from matplotlib.pyplot import imshow, subplot, show, axis

# Divide the examined window to cells (e.g. 16x16 pixels for each cell).

# For each pixel in a cell, compare the pixel to each of its 8 neighbors
# (on its left-top, left-middle, left-bottom, right-top, etc.). Follow the
# pixels along a circle, i.e. clockwise or counter-clockwise.

# Where the center pixel's value is greater than the neighbor, write "1".
# Otherwise, write "0". This gives an 8-digit binary number (which is usually
# converted to decimal for convenience).

# Compute the histogram, over the cell, of the frequency of each "number"
# occurring (i.e., each combination of which pixels are smaller and which are
# greater than the center).

# Optionally normalize the histogram. Concatenate normalized histograms of all
# cells. This gives the feature vector for the window.

CELL_SIZE = 16

def domain_iterator(shape):
    """Iterate over the pixels of an image."""
    for y in xrange(shape[0]):
        for x in xrange(shape[1]):
            yield y, x

image = array(Image.open('../images/test.png').convert('L'))

def in_image(y, x, F):
    """Check if given pixel coordinates are within the bounds of image F."""
    return 0 <= y < F.shape[0] and 0 <= x < F.shape[1]

def features(image):
    """Compare each pixel to each of its eight neigheach pixel to each of its
    eight neighbours."""
    features = zeros(image.shape, dtype=byte)

    def cmp_pixels(y, x, p):
        return in_image(y, x, image) and image[y, x] > p

    for y, x in domain_iterator(features.shape):
        p = image[y, x]

        # Walk around the pixel in counter-clokwise order, shifting 1 but less
        # at each neighbour starting at 7 in the top-left corner. This gives a
        # 8-bitmap
        features[y, x] = byte(cmp_pixels(y - 1, x - 1, p)) << 7 \
                         | byte(cmp_pixels(y - 1, x, p)) << 6 \
                         | byte(cmp_pixels(y - 1, x + 1, p)) << 5 \
                         | byte(cmp_pixels(y, x + 1, p)) << 4 \
                         | byte(cmp_pixels(y + 1, x + 1, p)) << 3 \
                         | byte(cmp_pixels(y + 1, x, p)) << 2 \
                         | byte(cmp_pixels(y + 1, x - 1, p)) << 1 \
                         | byte(cmp_pixels(y, x - 1, p))

    return features

def feature_vectors(image):
    """Create cell histograms of an image"""
    F = features(image)

V = feature_vectors(image)
subplot(121)
imshow(image, cmap='gray')
subplot(122)
imshow(V, cmap='gray')
axis('off')
show()
