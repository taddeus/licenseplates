from PIL import Image
from Pylab import *
from LBP import domain_iterator

THRESHOLD = 0.5

im = Image.open('../.jpg')
im = Image.convert('L', im)

outer_bounds = get_outer_bounds()

im.crop(outer_bounds)

imshow(im)

show()

def get_outer_bound():
    min_x = len(im[0])
    max_x = 0
    min_y = len(im)
    max_y = 0

    for y in xrange(len(im)):
        for x in xrange(len(im[0])):
            if im[y, x] > THRESHOLD:
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y
    return (min_x, min_y, max_x, max_y)
            
        
    
    
    
