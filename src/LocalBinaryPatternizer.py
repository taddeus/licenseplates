from Histogram import Histogram
from numpy import zeros, byte
from math import ceil

class LocalBinaryPatternizer:
        
    def __init__(self, image, cell_size=16):
        self.cell_size = cell_size
        self.image = image
        self.setup_histograms()

        
    def setup_histograms(self):
        cells_in_width = int(ceil(self.image.width / float(self.cell_size)))
        cells_in_height = int(ceil(self.image.height / float(self.cell_size)))
        self.features = []
        for i in xrange(cells_in_height):
            self.features.append([])
            for j in xrange(cells_in_width):
                self.features[i].append(Histogram(256,0,256))

                
    def create_features_vector(self):
        ''' Walk around the pixels in clokwise order, shifting 1 bit less
            at each neighbour starting at 7 in the top-left corner. This gives a
            8-bit feature number of a pixel'''
        for y, x, value in self.image:
            
            pattern = (self.is_pixel_darker(y - 1, x - 1, value) << 7) \
                    | (self.is_pixel_darker(y - 1, x    , value) << 6) \
                    | (self.is_pixel_darker(y - 1, x + 1, value) << 5) \
                    | (self.is_pixel_darker(y    , x + 1, value) << 4) \
                    | (self.is_pixel_darker(y + 1, x + 1, value) << 3) \
                    | (self.is_pixel_darker(y + 1, x    , value) << 2) \
                    | (self.is_pixel_darker(y + 1, x - 1, value) << 1) \
                    | (self.is_pixel_darker(y    , x - 1, value) << 0)
                    
            cy, cx = self.get_cell_index(y, x)
            self.features[cy][cx].add(pattern)

        return self.get_features_as_array()
    
    
    def is_pixel_darker(self, y, x, value):
        return self.image.in_bounds(y, x) and self.image[y, x] > value
        
        
    def get_cell_index(self, y, x):
        return (y / self.cell_size, x / self.cell_size)
        
        
    def get_features_as_array(self):
        return [item for sublist in self.features for item in sublist]
