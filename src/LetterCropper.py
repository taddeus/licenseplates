from Rectangle import Rectangle

class LetterCropper:

    def __init__(self, image, threshold = 0.9):
        self.set_image(image)
        self.set_threshold(threshold)
        
    def set_image(self, image):
        self.image = image
        
    def set_threshold(self, threshold):
        self.threshold = threshold
                
    def get_cropped_letter(self):
        self.determine_letter_bounds()
        self.image.crop(self.letter_bounds)
        return self.image

    def determine_letter_bounds(self):
    
        min_x = self.image.width
        max_x = 0
        min_y = self.image.height
        max_y = 0

        for y in xrange(self.image.height):
            for x in xrange(self.image.width):
                if self.image[y, x] < self.threshold:
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

