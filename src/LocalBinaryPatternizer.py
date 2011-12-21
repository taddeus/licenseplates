from Histogram import Histogram
from math import ceil

class LocalBinaryPatternizer:
    """This class generates a Local Binary Pattern of a given image."""
    
    def __init__(self, image, cell_size=16, neighbours=3):
        self.cell_size = cell_size
        self.image = image
        self.pattern_callback, self.bins = {
                    3: (self.pattern_3x3, 256),
                    5: (self.pattern_5x5, 4096)
                }[neighbours]

    def setup_histograms(self):
        cells_in_width = int(ceil(self.image.width / float(self.cell_size)))
        cells_in_height = int(ceil(self.image.height / float(self.cell_size)))
        self.histograms = []

        for i in xrange(cells_in_height):
            self.histograms.append([])

            for j in xrange(cells_in_width):
                self.histograms[i].append(Histogram(self.bins, 0, self.bins))

    def pattern_3x3(self, y, x, value):
        """Create the Local Binary Pattern in the (8,3)-neighbourhood."""
        return (self.is_pixel_darker(y - 1, x - 1, value) << 7) \
             | (self.is_pixel_darker(y - 1, x    , value) << 6) \
             | (self.is_pixel_darker(y - 1, x + 1, value) << 5) \
             | (self.is_pixel_darker(y    , x + 1, value) << 4) \
             | (self.is_pixel_darker(y + 1, x + 1, value) << 3) \
             | (self.is_pixel_darker(y + 1, x    , value) << 2) \
             | (self.is_pixel_darker(y + 1, x - 1, value) << 1) \
             | (self.is_pixel_darker(y    , x - 1, value))

    def pattern_5x5_hybrid(self, y, x, value):
        """Create the Local Binary Pattern in the (8,5)-neighbourhood."""
        return (self.is_pixel_darker(y - 2, x - 2, value) << 7) \
             | (self.is_pixel_darker(y - 2, x    , value) << 6) \
             | (self.is_pixel_darker(y - 2, x + 2, value) << 5) \
             | (self.is_pixel_darker(y    , x + 2, value) << 4) \
             | (self.is_pixel_darker(y + 2, x + 2, value) << 3) \
             | (self.is_pixel_darker(y + 2, x    , value) << 2) \
             | (self.is_pixel_darker(y + 2, x - 2, value) << 1) \
             | (self.is_pixel_darker(y    , x - 2, value))

    def pattern_5x5(self, y, x, value):
        """Create the Local Binary Pattern in the (12,5)-neighbourhood."""
        return (self.is_pixel_darker(y - 1, x - 2, value) << 11) \
             | (self.is_pixel_darker(y    , x - 2, value) << 10) \
             | (self.is_pixel_darker(y + 1, x - 2, value) << 9) \
             | (self.is_pixel_darker(y + 2, x - 1, value) << 8) \
             | (self.is_pixel_darker(y + 2, x    , value) << 7) \
             | (self.is_pixel_darker(y + 2, x + 1, value) << 6) \
             | (self.is_pixel_darker(y + 1, x + 2, value) << 5) \
             | (self.is_pixel_darker(y    , x + 2, value) << 4) \
             | (self.is_pixel_darker(y - 1, x + 2, value) << 3) \
             | (self.is_pixel_darker(y - 2, x + 1, value) << 2) \
             | (self.is_pixel_darker(y - 2, x    , value) << 1) \
             | (self.is_pixel_darker(y - 2, x - 1, value))

    def create_features_vector(self):
        '''Walk around the pixels in clockwise order, shifting 1 bit less at
        each neighbour starting at 7 in the top-left corner. This gives a 8-bit
        feature number of a pixel'''
        self.setup_histograms()

        for y, x, value in self.image:
            cy, cx = self.get_cell_index(y, x)
            self.histograms[cy][cx].add(self.pattern_callback(y, x, value))

        return self.get_features_as_array()

    def is_pixel_darker(self, y, x, value):
        return self.image.in_bounds(y, x) and self.image[y, x] > value

    def get_cell_index(self, y, x):
        return (y / self.cell_size, x / self.cell_size)

    def get_features_as_array(self):
        f = []

        # Concatenate all histogram bins
        for row in self.histograms:
            for hist in row:
                f.extend(hist.bins)

        return f

    def get_single_histogram(self):
        """Create a single histogram of the local binary patterns in the
        image."""
        h = Histogram(self.bins, 0, self.bins)

        for y, x, value in self.image:
            h.add(self.pattern_callback(y, x, value))

        h.normalize()

        return h

    def single_cell_features_vector(self):
        return self.get_single_histogram().bins
