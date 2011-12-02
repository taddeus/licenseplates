from copy import deepcopy
from GrayscaleImage import GrayscaleImage
from LetterCropper import LetterCropper
from GaussianFilter import GaussianFilter

class NormalizedCharacterImage(GrayscaleImage):
    
    def __init__(self, image=None, data=None, size=(60, 40), blur=1.1, crop_threshold=0.9):
        if image != None:
            GrayscaleImage.__init__(self, data=deepcopy(image.data))
        elif data != None:
            GrayscaleImage.__init__(self, data=deepcopy(data))
        self.blur = blur
        self.crop_threshold = crop_threshold
        self.size = size
        self.gausse_filter()
        self.increase_contrast()
        self.crop_to_letter()
        self.resize()

    def increase_contrast(self):
        self.data -= self.data.min()
        self.data /= self.data.max()

    def gausse_filter(self):    
        filter = GaussianFilter(1.1)
        filter.filter(self)
        
    def crop_to_letter(self):
        cropper = LetterCropper(0.9)
        cropper.crop_to_letter(self)

    def resize(self):
        GrayscaleImage.resize(self, self.size)