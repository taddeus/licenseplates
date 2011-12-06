from GrayscaleImage import GrayscaleImage
from scipy.ndimage import gaussian_filter

class GaussianFilter:

    def __init__(self, scale):
        self.scale = scale

    def get_filtered_copy(self, image):
        """Apply a gaussian blur to an image, to suppress noise."""
        image = gaussian_filter(image.data, self.scale)
        return GrayscaleImage(None, image)

    def filter(self, image):
        image.data = gaussian_filter(image.data, self.scale)

    def get_scale(self):
      return self.scale

    def set_scale(self, scale):
        self.scale = float(scale)

    scale = property(get_scale, set_scale)
