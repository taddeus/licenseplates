from LetterCropper import LetterCropper
from GrayscaleImage import GrayscaleImage

image = GrayscaleImage("../images/test.png")

cropper = LetterCropper(image)

cropped_letter = cropper.get_cropped_letter()

cropped_letter.show()
