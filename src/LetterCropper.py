from copy import deepcopy
from Rectangle import Rectangle

class LetterCropper:

    def __init__(self, threshold = 0.9):
        self.source_image = image
        self.threshold = threshold
        
    def get_cropped_letter(self):
        self.determine_letter_bounds()
        self.result_image = deepcopy(self.source_image)
        self.result_image.crop(self.letter_bounds)
        return self.result_image

    def determine_letter_bounds(self):
        min_x = self.source_image.width
        max_x = 0
        min_y = self.source_image.height
        max_y = 0

        for y, x, value in self.source_image:
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
