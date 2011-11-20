from pylab import *

class GrayscaleImage:

    def __init__(self, image_path = None, data = None):
        if image_path != None:
            self.data = imread(image_path)
            self.convert_to_grayscale()
        elif data != None:
            self.data = data
    
    def __iter__(self):
        self.i_x = -1
        self.i_y = 0
        return self
            
    def next(self):
        self.i_x += 1
        if self.i_x  == self.width:
            self.i_x = 0
            self.i_y += 1
        elif self.i_y == self.height:
            raise StopIteration
        else:
            return self[self.i_y, self.i_x]
            
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
    
    def get_width(self):
        return len(self.data[0])
        
    def get_height(self):
        return len(self.data)
    
    width = property(get_width)
    height = property(get_height)
    
