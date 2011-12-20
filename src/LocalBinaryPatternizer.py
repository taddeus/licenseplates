from Histogram import Histogram
from math import ceil

class LocalBinaryPatternizer:

    def __init__(self, image, cell_size=16):
        self.cell_size = cell_size
        self.image = image

    def setup_histograms(self):
        cells_in_width = int(ceil(self.image.width / float(self.cell_size)))
        cells_in_height = int(ceil(self.image.height / float(self.cell_size)))
        self.histograms = []

        for i in xrange(cells_in_height):
            self.histograms.append([])

            for j in xrange(cells_in_width):
                self.histograms[i].append(Histogram(256, 0, 256))

    def local_binary_pattern(self, y, x, value):
        return (self.is_pixel_darker(y - 1, x - 1, value) << 7) \
             | (self.is_pixel_darker(y - 1, x    , value) << 6) \
             | (self.is_pixel_darker(y - 1, x + 1, value) << 5) \
             | (self.is_pixel_darker(y    , x + 1, value) << 4) \
             | (self.is_pixel_darker(y + 1, x + 1, value) << 3) \
             | (self.is_pixel_darker(y + 1, x    , value) << 2) \
             | (self.is_pixel_darker(y + 1, x - 1, value) << 1) \
             | (self.is_pixel_darker(y    , x - 1, value) << 0)

    def create_features_vector(self):
        '''Walk around the pixels in clokwise order, shifting 1 bit less at
        each neighbour starting at 7 in the top-left corner. This gives a 8-bit
        feature number of a pixel'''
        self.setup_histograms()

        for y, x, value in self.image:
            cy, cx = self.get_cell_index(y, x)
            self.histograms[cy][cx].add(self.local_binary_pattern(y, x, value))

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
        #return [h.bins for h in [h for sub in self.histograms for h in sub]][0]

    def get_single_histogram(self):
        """Create a single histogram of the local binary patterns in the
        image."""
        h = Histogram(256, 0, 256)

        for y, x, value in self.image:
            h.add(self.local_binary_pattern(y, x, value))

        h.normalize()

        return h

    def single_cell_features_vector(self):
        return self.get_single_histogram().bins
