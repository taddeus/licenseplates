from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage 
from LetterCropper import LetterCropper

image = GrayscaleImage("../images/test10.png")
normalized_character_image = NormalizedCharacterImage(image)
normalized_character_image.show()