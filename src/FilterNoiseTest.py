from FilterNoise import filterNoise
from GrayscaleImage import GrayscaleImage

# Get the image
image = GrayscaleImage('../images/plate.png')

output_image = filterNoise(image, 1.4)

# Show the licenseplate                 
output_image = GrayscaleImage(None, output_image)
output_image.show()
