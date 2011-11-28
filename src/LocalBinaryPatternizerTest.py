from GrayscaleImage import GrayscaleImage
from LocalBinaryPatternizer import LocalBinaryPatternizer
from LetterCropper import LetterCropper
from matplotlib.pyplot import imshow, subplot, show, axis, bar
from numpy import arange

image = GrayscaleImage("../images/test.png")

lbp = LocalBinaryPatternizer(image)
histograms = lbp.create_features_vector()

print histograms