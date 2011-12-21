#!/usr/bin/python
from os import listdir
from cPickle import load
from sys import argv, exit
from time import time

from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from Character import Character
from Classifier import Classifier

if len(argv) < 4:
    print 'Usage: python %s NEIGHBOURS BLUR_SCALE COUNT' % argv[0]
    exit(1)

neighbours = int(argv[1])
blur_scale = float(argv[2])
count = int(argv[3])
suffix = '_%s_%s' % (blur_scale, neighbours)

#chars_file = 'characters%s.dat' % suffix
classifier_file = 'classifier%s.dat' % suffix

#print 'Loading characters...'
#chars = load(open(chars_file, 'r'))[:count]
#count = len(chars)
#
#for char in chars:
#    del char.feature
#
#print 'Read %d characters' % count

print 'Loading %d characters...' % count
chars = []
i = 0
br = False

for value in sorted(listdir('../images/LearningSet')):
    for image in sorted(listdir('../images/LearningSet/' + value)):
        f = '../images/LearningSet/' + value + '/' + image
        image = GrayscaleImage(f)
        char = Character(value, [], image)
        chars.append(char)
        i += 1

        if i == count:
            br = True
            break

    if br:
        break

print 'Loading classifier...'
classifier = Classifier(filename=classifier_file)
classifier.neighbours = neighbours

start = time()

for char in chars:
    char.image = NormalizedCharacterImage(image, blur=blur_scale, height=42)
    char.get_single_cell_feature_vector(neighbours)
    classifier.classify(char)

elapsed = time() - start
individual = elapsed / count

print 'Took %fs to classify %d caracters (%fms per character)' \
        % (elapsed, count, individual * 1000)
