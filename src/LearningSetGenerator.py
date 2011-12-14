from xml_helper_functions import xml_to_LicensePlate

for i in range(1):
    for j in range(1):

            filename = '%04d/00991_%04d%02d' % (i, i, j)
            print 'loading file "%s"' % filename

            plate = xml_to_LicensePlate(filename, save_character=1)
            print plate.characters[0].value;