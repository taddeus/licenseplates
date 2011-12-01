from GetPlate import getPlateAt
from GrayscaleImage import GrayscaleImage
from Point import Point

# Define the corners of the licenseplate
points = [Point(None, (310, 383)), \
          Point(None, (382, 381)), \
          Point(None, (382, 396)), \
          Point(None, (310, 398))]

# Get the image
image = GrayscaleImage('../images/test_plate.png')

# Let the code get the licenseplate
output_image = getPlateAt(image, points, 100, 20)

# Show the licenseplate                 
output_image = GrayscaleImage(None, output_image)
output_image.show()
