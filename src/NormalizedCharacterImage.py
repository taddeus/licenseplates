from copy import deepcopy
from GrayscaleImage import GrayscaleImage
from GaussianFilter import GaussianFilter

class NormalizedCharacterImage(GrayscaleImage):

    def __init__(self, image=None, data=None, height=None, blur=1.1):
        if image != None:
            GrayscaleImage.__init__(self, data=deepcopy(image.data))
        elif data != None:
            GrayscaleImage.__init__(self, data=deepcopy(data))

        self.height = height
        self.resize()

        self.blur = blur
        self.gaussian_filter()

    def gaussian_filter(self):
        GaussianFilter(self.blur).filter(self)

    def resize(self):
        """Resize the image to a fixed height."""
        if self.height == None:
            return

        h, w = self.data.shape
        GrayscaleImage.resize(self, (self.height, self.height * w / h))
