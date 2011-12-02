from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage 

# Comment added by Richard Torenvliet
# Steps in this test files are
# 1. crop image 
# 2. resize to default hight (in future also to width)
# 3. plot

image = GrayscaleImage("../images/test10.png")
normalized_character_image = NormalizedCharacterImage(image)
normalized_character_image.show()
