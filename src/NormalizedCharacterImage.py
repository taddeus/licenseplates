from copy import deepcopy
from GrayscaleImage import GrayscaleImage
from LetterCropper import LetterCropper
from GaussianFilter import GaussianFilter

class NormalizedCharacterImage(GrayscaleImage):

    def __init__(self, image=None, data=None, size=(60, 40), blur=1.1, \
            crop_threshold=0.9):
        if image != None:
            GrayscaleImage.__init__(self, data=deepcopy(image.data))
        elif data != None:
            GrayscaleImage.__init__(self, data=deepcopy(data))
        self.blur = blur
        self.crop_threshold = crop_threshold
        self.size = size
        self.gaussian_filter()
        self.increase_contrast()
        #self.crop_to_letter()
        #self.resize()

    def increase_contrast(self):
        self.data -= self.data.min()
        self.data = self.data.astype(float) / self.data.max()

    def gaussian_filter(self):
        GaussianFilter(self.blur).filter(self)

    def crop_to_letter(self):
        cropper = LetterCropper(0.9)
        cropper.crop_to_letter(self)

    def resize(self):
        GrayscaleImage.resize(self, self.size)
