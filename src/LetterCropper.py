from copy import deepcopy
from Rectangle import Rectangle
from GrayscaleImage import GrayscaleImage

class LetterCropper:

    def __init__(self, threshold = 0.9):
        self.threshold = threshold
        
    def crop_to_letter(self, image):
        self.image = image
        self.determine_letter_bounds()
        self.image.crop(self.letter_bounds)

    def determine_letter_bounds(self):
        min_x = self.image.width
        max_x = 0
        min_y = self.image.height
        max_y = 0

        for y, x, value in self.image:
            if value < self.threshold:
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y
        
        self.letter_bounds = Rectangle(
            min_x, 
            min_y, 
            max_x - min_x ,
            max_y - min_y
        )
