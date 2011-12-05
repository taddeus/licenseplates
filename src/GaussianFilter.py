from GrayscaleImage import GrayscaleImage
from scipy.ndimage import gaussian_filter
from pylab import ceil, zeros, pi, exp, sqrt, array

class GaussianFilter:

    def __init__(self, scale):
        self.scale = scale

    def gaussian(self, x):
        """Return the value of a 1D Gaussian function for a given x."""
        return exp(-(x ** 2 / (2 * self.scale ** 2))) \
               / (sqrt(2 * pi) * self.scale)

    def get_1d_gaussian_kernel(self):
        """Sample a one-dimensional Gaussian function of scale s."""
        radius = int(ceil(3 * self.scale))
        size = 2 * radius + 1

        result = zeros(size)
        # Sample the Gaussian function
        result = array([self.gaussian(x - radius) for x in xrange(size)])
        # The sum of all kernel values is equal to one
        result /= result.sum()

        return result

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
