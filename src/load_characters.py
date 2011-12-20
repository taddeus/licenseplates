#!/usr/bin/python
from os import listdir
from cPickle import dump
from sys import argv, exit

from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from Character import Character

if len(argv) < 4:
    print 'Usage: python %s FILE_SUFFIX BLUR_SCALE NEIGHBOURS' % argv[0]
    exit(1)

c = []

for char in sorted(listdir('../images/LearningSet')):
    for image in sorted(listdir('../images/LearningSet/' + char)):
        f = '../images/LearningSet/' + char + '/' + image
        image = GrayscaleImage(f)
        norm = NormalizedCharacterImage(image, blur=float(argv[2]), height=42)
        #from pylab import imshow, show
        #imshow(norm.data, cmap='gray'); show()
        character = Character(char, [], norm)
        character.get_single_cell_feature_vector(int(argv[3]))
        c.append(character)
        print char

print 'Saving characters...'
dump(c, open('characters%s.dat' % argv[1], 'w+'))
