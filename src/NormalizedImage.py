from PIL import Image

class NormalizedImage:
    DEFAULT_SIZE = (100, 200)

    def __init__(self, image, size):
        self.letter = image

        if size:
            self.size = size
        else:
            self.size = self.DEFAULT_SIZE

        self.add_padding()
        self.resize()

    def add_padding(self):
        pass

    def resize(self):
        return self.letter.resize(self.size, Image.NEAREST)
