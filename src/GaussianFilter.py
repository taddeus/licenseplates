from GrayscaleImage import GrayscaleImage
from scipy.ndimage import gaussian_filter

class GaussianFilter:
    """This class can apply a Gaussian blur on an image."""

    def __init__(self, scale):
        """Create a GaussianFilter object with a given scale."""
        self.scale = scale

    def get_filtered_copy(self, image):
        """Apply a gaussian blur to an image, to suppress noise."""
        image = gaussian_filter(image.data, self.scale)
        return GrayscaleImage(None, image)

    def filter(self, image):
        """Apply a Gaussian blur on the image data."""
        image.data = gaussian_filter(image.data, self.scale)

    def get_scale(self):
        """Return the scale of the Gaussian kernel."""
        return self.scale

    def set_scale(self, scale):
        """Set the scale of the Gaussian kernel."""
        self.scale = float(scale)

    scale = property(get_scale, set_scale)
