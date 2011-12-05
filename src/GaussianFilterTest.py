from GaussianFilter import GaussianFilter
from GrayscaleImage import GrayscaleImage

image = GrayscaleImage('../images/plate.png')

filter = GaussianFilter(1.4)
output_image = filter.get_filtered_copy(image)

output_image.show()
