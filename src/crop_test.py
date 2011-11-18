from pylab import *
from crop import LetterCropper

letter_cropper = LetterCropper("../images/test.png")
cropped_letter = letter_cropper.get_cropped_letter()

imshow(cropped_letter, cmap="gray")

show()


