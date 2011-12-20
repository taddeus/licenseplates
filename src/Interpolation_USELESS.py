from pylab import floor

def pV(image, x, y):
    '''Get the value of a point x,y in the given image, where x and y are not
    necessary integers, so the value is interpolated from its neighbouring
    pixels.'''
    if inImage(image, x, y):
        x_low = floor(x)
        x_high = floor(x + 1)
        y_low = floor(y)
        y_high = floor(y + 1)
        x_y = (x_high - x_low) * (y_high - y_low)
        
        interpolatedValue = image[x_low, y_low] / x_y * (x_high - x) * \
                                (y_high - y)\
                          + image[x_high][y_low] / x_y * (x - x_low) * \
                                (y_high - y)\
                          + image[x_low][y_high] / x_y * (x_high - x) * \
                                (y - y_low)\
                          + image[x_high][y_high] / x_y * (x - x_low) * \
                                (y - y_low)
        return interpolatedValue
    else:
        constantValue = 0
        return constantValue
    
def inImage(image, x, y):
    '''Return if the pixels is within the image bounds.'''
    return (x > 0 and x < image.get_height() - 1 \
        and y > 0 and y < image.get_width() - 1)
