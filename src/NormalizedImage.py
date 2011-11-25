from copy import deepcopy
class NormalizedImage:
    
    DEFAULT_SIZE = 100.0
    
    def __init__(self, image, size=DEFAULT_SIZE):
        self.source_image = image
        self.size = size

    def add_padding(self):
        pass

    # normalize img
    def get_normalized_letter(self):
        self.result_image = deepcopy(self.source_image)
        self.result_image.resize(self.size / self.source_image.height)
        return self.result_image
