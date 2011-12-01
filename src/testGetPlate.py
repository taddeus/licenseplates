from GetPlate import getPlateAt
from pylab import imread, imshow, show, figure
from GrayscaleImage import GrayscaleImage

# Define the coordinates of the licenseplate
x_vals = [310, 382, 382, 310]
y_vals = [383, 381, 396, 398]

# Get the image
image = GrayscaleImage('../images/test_plate.png')

# Let the code get the licenseplate
output_image = getPlateAt(image, x_vals[0], y_vals[0],\
                                 x_vals[1], y_vals[1],\
                                 x_vals[2], y_vals[2],\
                                 x_vals[3], y_vals[3], 100, 20)

# Show the licenseplate                 
output_image = GrayscaleImage(None, output_image)
output_image.show()
