from scipy.ndimage import convolve1d
from pylab import ceil, zeros, pi, e, exp, sqrt, array

def f(x, s):
    """Return the value of a 1D Gaussian function for a given x and scale."""
    return exp(-(x ** 2 / (2 * s ** 2))) / (sqrt(2 * pi) * s)

                                                             
def gauss1(s, order=0):
    """Sample a one-dimensional Gaussian function of scale s."""
    s = float(s)
    r = int(ceil(3 * s))
    size = 2 * r + 1
    W = zeros(size)

    # Sample the Gaussian function
    W = array([f(x - r, s) for x in xrange(size)])

    if not order:
        # Make sure that the sum of all kernel values is equal to one
        W /= W.sum()

    return W
    
def filterNoise(image, s):
    '''Apply a gaussian blur to an image, to suppress noise.'''
    filt = gauss1(s)
    image = convolve1d(image.data, filt, axis=0, mode='nearest')
    return convolve1d(image, filt, axis=1, mode='nearest')
