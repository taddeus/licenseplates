from GrayscaleImage import GrayscaleImage
from LocalBinaryPatternizer import LocalBinaryPatternizer
from LetterCropper import LetterCropper
from matplotlib.pyplot import imshow, subplot, show, axis
from NormalizedImage import NormalizedImage
from GaussianFilter import GaussianFilter

# Comment added by Richard Torenvliet
# Steps in this test files are
# 1. crop image 
# 2. resize to default hight (in future also to width)
# 3. preform LBP
# 4. construct feature vector
# 5. plot

# Image is now an instance of class GrayscaleImage
# GrayscaleImage has functions like resize, crop etc.
image = GrayscaleImage("../images/test9.png")
filter = GaussianFilter(1.4)

image = filter.get_filtered_copy(image)

# Crops image; param threshold is optional: LetterCropper(image, threshold=0.9)
# image: GrayscaleImage, threshold: float

cropper = LetterCropper(image, 0.7)
cropped_letter = cropper.get_cropped_letter()

# Show difference in shape
print cropped_letter.shape

# Resizes image; param size is optional: NormalizedImage(image, size=DEFAULT)
# image: GrayscaleImage, size: float
norm = NormalizedImage(cropped_letter)
resized = norm.get_normalized_letter()

print resized.show()

show()
# Difference is noticable
print resized.shape

lbp = LocalBinaryPatternizer(resized)

feature_vector = lbp.create_features_vector()
print feature_vector
feature_vector /= 255 # Prepare for displaying -> 0 - 255 -> 0 - 1
        
subplot(141)
imshow(image.data, cmap='gray')

subplot(142)
imshow(cropped_letter.data, cmap='gray')

subplot(143)
imshow(resized.data, cmap='gray')
subplot(144)
imshow(feature_vector, cmap='gray')

axis('off')
show()
