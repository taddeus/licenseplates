#!/usr/bin/python
from os import listdir
from sys import argv, exit
from time import time

from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from Character import Character
from data import IMAGES_FOLDER
from create_classifier import load_classifier

if len(argv) < 4:
    print 'Usage: python %s NEIGHBOURS BLUR_SCALE COUNT' % argv[0]
    exit(1)

neighbours = int(argv[1])
blur_scale = float(argv[2])
count = int(argv[3])

print 'Loading %d characters...' % count
chars = []
i = 0
br = False

for value in sorted(listdir()):
    for image in sorted(listdir(IMAGES_FOLDER + value)):
        f = IMAGES_FOLDER + value + '/' + image
        image = GrayscaleImage(f)
        char = Character(value, [], image)
        chars.append(char)
        i += 1

        if i == count:
            br = True
            break

    if br:
        break

# Load classifier
classifier = load_classifier(neighbours, blur_scale, verbose=1)

# Measure the time it takes to recognize <count> characters
start = time()

for char in chars:
    char.image = NormalizedCharacterImage(image, blur=blur_scale, height=42)
    char.get_single_cell_feature_vector(neighbours)
    classifier.classify(char)

elapsed = time() - start
individual = elapsed / count

print 'Took %fs to classify %d caracters (%fms per character)' \
        % (elapsed, count, individual * 1000)
