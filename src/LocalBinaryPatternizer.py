from numpy import zeros, byte

class LocalBinaryPatternizer:

    def __init__(self, image, cell_size = 16):
        self.cell_size = cell_size
        self.image = image
        self.features = zeros(self.image.shape)
        
    def create_features_vector(self):
        ''' Walk around the pixels in clokwise order, shifting 1 bit less
            at each neighbour starting at 7 in the top-left corner. This gives a
            8-bit feature number of a pixel'''
        for y, x, value in self.image:
            self.features[y, x] = \
                  (self.is_pixel_darker(y - 1, x - 1, value) << 7) \
                | (self.is_pixel_darker(y - 1, x    , value) << 6) \
                | (self.is_pixel_darker(y - 1, x + 1, value) << 5) \
                | (self.is_pixel_darker(y    , x + 1, value) << 4) \
                | (self.is_pixel_darker(y + 1, x + 1, value) << 3) \
                | (self.is_pixel_darker(y + 1, x    , value) << 2) \
                | (self.is_pixel_darker(y + 1, x - 1, value) << 1) \
                | (self.is_pixel_darker(y    , x - 1, value) << 0)

        return self.features
    
    def is_pixel_darker(self, y, x, value):
        return self.image.in_bounds(y, x) and self.image[y, x] > value
