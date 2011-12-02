from LicensePlate import LicensePlate

'''
 create new LicensePlate object:

 i.e you can do 

 plate = LicensePlate("../XML/test.info") # some xml file from rein

 now available:

 plate.image
 plate.width
 plate.height

 Are the entire image widht / height and image is the corresponding image file
 provided by rein (i.e other folder somewhere)

 plate.corners
 
 plate.license_full  # the entire license plate as a string so 2334AB
 plate.characters    # for each character from license_full a Character object
                       exists, kinda same as the license plate. You have a value
                       = the character / number

                       a corners -> i.e list of points (Point objects)

  TODO had to go so this text is full of crap maybe, anyway enjoy
 
'''

plate = LicensePlate("../XML/0000/00991_000000.info") # some xml file from rein

print plate.characters[0].value
#plate.characters[0].show()