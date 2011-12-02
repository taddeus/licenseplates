from copy import deepcopy
from GrayscaleImage import GrayscaleImage
from LetterCropper import LetterCropper
from GaussianFilter import GaussianFilter

class NormalizedCharacterImage(GrayscaleImage):
    
    def __init__(self, image, size=(60, 40), blur=1.1, crop_threshold=0.9):
        GrayscaleImage.__init__(self, data=deepcopy(image.data))
        self.blur = blur
        self.crop_threshold = crop_threshold
        self.size = size
        self.gausse_filter()
        self.increase_contrast()
        self.crop()
        self.resize()

    def increase_contrast(self):
        self.data -= self.data.min()
        self.data /= self.data.max()

    def gausse_filter(self):    
        filter = GaussianFilter(1.1)
        filter.filter(self)
        
    def crop(self):
        cropper = LetterCropper(self, 0.9)
        self.data = cropper.get_cropped_letter().data

    def resize(self):
        self.resize(self.size)
