from copy import deepcopy
from GrayscaleImage import GrayscaleImage
from LetterCropper import LetterCropper
from GaussianFilter import GaussianFilter
from numpy import resize, array, append, vstack, hstack, zeros

class CharacterImageNormalizer:

    def __init__(self, size=(60, 40), blur=1.1, crop_threshold=126):
        self.size = size
        self.gausse_filter = GaussianFilter(blur)
        self.cropper = LetterCropper(crop_threshold)
        
    def normalize(self, image):
        self.gausse_filter.filter(image)
        GrayscaleImage.resize(image, (60,  60 / image.height * image.width))
        self.increase_contrast(image)
        self.to_black_white(image, 30)
        self.cropper.crop_to_letter(image)
        self.add_padding(image)

    def add_padding(self, image):
        data = array(image.data)
         
        top_bottom_padding = zeros((3, data.shape[1])) 
        data = vstack((top_bottom_padding, data))
        data = vstack((data, top_bottom_padding))
        
        left_right_padding = zeros((data.shape[0], 3))
        data = hstack((left_right_padding, data))
        data = hstack((data, left_right_padding))

        extra_left_padding = zeros((data.shape[0], data.shape[0] - data.shape[1]))
        data = hstack((extra_left_padding, data))
          
        image.data = data

    def increase_contrast(self, image):
        image.data -= image.data.min()
        image.data /= image.data.max() / 255.0

    def to_black_white(self, image, bla):
        for y, x, value in image:
            image.data[y, x] = 255 if value < bla else 0