from GrayscaleImage import GrayscaleImage
from LocalBinaryPatternizer import LocalBinaryPatternizer

image = GrayscaleImage("../images/test.png")

lbp = LocalBinaryPatternizer(image)
histograms = lbp.create_features_vector()

print histograms
