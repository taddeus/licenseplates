from pylab import *

class LetterCropper:

    THRESHOLD = 0.5

    def __init__(self, image_path):
        self.set_image(image_path)
        
    def set_image(self, image_path):
        self.source_image = imread(image_path)
                
    def get_cropped_letter(self):
        self.convert_image_to_grayscale()
        self.determine_letter_bounds()
        self.crop_image()
        return self.cropped_letter

    def convert_image_to_grayscale(self):
        self.cropped_letter = self.source_image.sum(axis=2) / 3

    def determine_letter_bounds(self):
        image_width = len(self.cropped_letter[0])
        image_height = len(self.cropped_letter)
    
        min_x = image_width
        max_x = 0
        min_y = image_height
        max_y = 0

        for y in xrange(image_height):
            for x in xrange(image_width):
                if self.cropped_letter[y, x] < self.THRESHOLD:
                    if x < min_x: min_x = x
                    if y < min_y: min_y = y
                    if x > max_x: max_x = x
                    if y > max_y: max_y = y
        
        self.letter_bounds = (min_x, min_y, max_x, max_y)
        
    def crop_image(self):
        self.cropped_letter = self.cropped_letter[self.letter_bounds[1] : self.letter_bounds[3], 
                                                  self.letter_bounds[0] : self.letter_bounds[2]]

