from pylab import imshow, imread, show

class GrayscaleImage:

    def __init__(self, image_path = None, data = None):
        if image_path != None:
            self.data = imread(image_path)
            self.convert_to_grayscale()
        elif data != None:
            self.data = data
    
    def __iter__(self):
        self.__i_x = -1
        self.__i_y = 0
        return self
            
    def next(self):
        self.__i_x += 1
        if self.__i_x  == self.width:
            self.__i_x = 0
            self.__i_y += 1
        if self.__i_y == self.height:
            raise StopIteration
        
        return  self.__i_y, self.__i_x, self[self.__i_y, self.__i_x]
            
    def __getitem__(self, position):
        return self.data[position]
        
    def convert_to_grayscale(self):
        self.data = self.data.sum(axis=2) / 3
        
    def crop(self, rectangle):
        self.data = self.data[rectangle.y : rectangle.y + rectangle.height, 
                              rectangle.x : rectangle.x + rectangle.width]
                              
    def show(self):
        imshow(self.data, cmap="gray")
        show()
    
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