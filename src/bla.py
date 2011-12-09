#!/usr/bin/python
from LicensePlate import LicensePlate
from Classifier import Classifier
from cPickle import dump, load

chars = []

for i in range(9):
    for j in range(100):
        filename = '%04d/00991_%04d%02d.info' % (i, i, j)
        plate = LicensePlate(i, j)
        if hasattr(plate, 'characters'):
            chars = plate.characters
           
        for char in chars:
            char.image.show()
        