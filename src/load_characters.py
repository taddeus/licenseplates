#!/usr/bin/python
from os import listdir
from cPickle import dump
from pylab import imshow, show

from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from Character import Character

c = []

for char in sorted(listdir('../images/LearningSet')):
    for image in sorted(listdir('../images/LearningSet/' + char)):
        f = '../images/LearningSet/' + char + '/' + image
        image = GrayscaleImage(f)
        norm = NormalizedCharacterImage(image, blur=1, size=(48, 36))
        #imshow(norm.data, cmap='gray')
        #show()
        character = Character(char, [], norm)
        character.get_single_cell_feature_vector()
        c.append(character)
        print char

dump(c, open('characters2', 'w+'))
