from GrayscaleImage import GrayscaleImage
from LocalBinaryPatternizer import LocalBinaryPatternizer
from LetterCropper import LetterCropper
from matplotlib.pyplot import imshow, subplot, show, axis

image = GrayscaleImage("../images/test.png")

cropper = LetterCropper(image)
cropped_letter = cropper.get_cropped_letter()

lbp = LocalBinaryPatternizer(cropped_letter)
feature_vector = lbp.create_features_vector()
feature_vector /= 255 # Prepare for displaying -> 0 - 255 -> 0 - 1
        
subplot(121)
imshow(image.data, cmap='gray')

subplot(122)
imshow(feature_vector, cmap='gray')

axis('off')
show()