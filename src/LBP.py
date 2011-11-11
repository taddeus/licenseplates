from pylab import imread, figure, show, imshow, zeros, axis

def to_grayscale(image):
    """Turn a RGB image to a grayscale image."""
    result = zeros(image.shape[:2])
    
    for x in xrange(len(image)):
        for y in xrange(len(image[0])):
            result[x][y] = image[x][y].sum() / 3
            
    return result
        
# Divide the examined window to cells (e.g. 16x16 pixels for each cell).

# For each pixel in a cell, compare the pixel to each of its 8 neighbors 
# (on its left-top, left-middle, left-bottom, right-top, etc.). Follow the 
# pixels along a circle, i.e. clockwise or counter-clockwise.
    
# Where the center pixel's value is greater than the neighbor, write "1". 
# Otherwise, write "0". This gives an 8-digit binary number (which is usually 
# converted to decimal for convenience).

# Compute the histogram, over the cell, of the frequency of each "number" 
# occurring (i.e., each combination of which pixels are smaller and which are 
# greater than the center).
    
# Optionally normalize the histogram. Concatenate normalized histograms of all 
# cells. This gives the feature vector for the window.

image = imread("../images/test.png")
image = to_grayscale(image)

figure()
imshow(image, cmap='gray')
axis('off')
show()
