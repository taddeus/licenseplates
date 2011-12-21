from pylab import imshow, imread, show
from matplotlib.pyplot import hist
from scipy.misc import imresize, imsave

class GrayscaleImage:

    def __init__(self, image_path = None, data = None):
        if image_path != None:
            self.data = imread(image_path)

            extension = image_path.split('.', 3)[-1]

            if extension == "jpg":
              self.data = self.data[::-1]

            self.convert_to_grayscale()
        elif data != None:
            self.data = data

    def __iter__(self):
        for y in xrange(self.data.shape[0]):
            for x in xrange(self.data.shape[1]):
                yield y, x, self.data[y, x]

    def __getitem__(self, position):
        return self.data[position]

    def convert_to_grayscale(self):
        if len(self.data.shape) > 2:
          self.data = self.data[:,:,:3].sum(axis=2) / 3

    def crop(self, rectangle):
        self.data = self.data[rectangle.y : rectangle.y + rectangle.height,
                              rectangle.x : rectangle.x + rectangle.width]

    def show(self):
        imshow(self.data, cmap="gray")
        show()

    def make_histogram(self):
        return hist(self.data)

    def resize(self, size):  # size is of type float
        self.data = imresize(self.data, size)

    def get_shape(self):
        return self.data.shape

    shape = property(get_shape)

    def get_width(self):
        return self.get_shape()[1]

    width = property(get_width)

    def get_height(self):
        return self.get_shape()[0]

    height = property(get_height)

    def in_bounds(self, y, x):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def save(self, path):
        imsave(path, self.data)
