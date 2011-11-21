from GrayscaleImage import GrayscaleImage
from LocalBinaryPatternizer import LocalBinaryPatternizer
from matplotlib.pyplot import imshow, subplot, show, axis

image = GrayscaleImage("../images/test.png")
lbp = LocalBinaryPatternizer(image)

feature_vector = lbp.create_features_vector()
feature_vector /= 255 # Prepare for displaying -> 0 - 255 -> 0 - 1
        
subplot(121)
imshow(image.data, cmap='gray')

subplot(122)
imshow(feature_vector, cmap='gray')

axis('off')
show()