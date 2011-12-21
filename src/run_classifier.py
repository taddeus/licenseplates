#!/usr/bin/python
from cPickle import load
from sys import argv, exit
from pylab import imsave, plot, subplot, imshow, show, axis, title
from math import sqrt, ceil
import os

from Classifier import Classifier

if len(argv) < 3:
    print 'Usage: python %s NEIGHBOURS BLUR_SCALE' % argv[0]
    exit(1)

neighbours = int(argv[1])
blur_scale = float(argv[2])
suffix = '_%s_%s' % (blur_scale, neighbours)

test_set_file = 'test_set%s.dat' % suffix
classifier_file = 'classifier%s.dat' % suffix

print 'Loading classifier...'
classifier = Classifier(filename=classifier_file)
classifier.neighbours = neighbours

print 'Loading test set...'
test_set = load(file(test_set_file, 'r'))
l = len(test_set)
matches = 0
#classified = {}
classified = []

for i, char in enumerate(test_set):
    prediction = classifier.classify(char, char.value)

    if char.value != prediction:
        classified.append((char, prediction))

        #key = '%s_as_%s' % (char.value, prediction)

        #if key not in classified:
        #    classified[key] = [char]
        #else:
        #    classified[key].append(char)

        print '"%s" was classified as "%s"' \
                % (char.value, prediction)
    else:
        matches += 1

    print '%d of %d (%d%% done)' % (i + 1, l, round(100 * (i + 1) / l))

print '\n%d matches (%d%%), %d fails' % (matches, \
        round(100 * matches / l), \
        len(test_set) - matches)

# Show a grid plot of all faulty classified characters
print 'Plotting faulty classified characters...'
rows = int(ceil(sqrt(l - matches)))
columns = int(ceil((l - matches) / float(rows)))

for i, pair in enumerate(classified):
    char, prediction = pair
    subplot(rows, columns, i + 1)
    title('%s as %s' % (char.value, prediction))
    imshow(char.image.data, cmap='gray')
    axis('off')

show()

#print 'Saving faulty classified characters...'
#folder = '../images/faulty/'
#
#if not os.path.exists(folder):
#    os.mkdir(folder)
#
#for filename, chars in classified.iteritems():
#    if len(chars) == 1:
#        imsave('%s%s' % (folder, filename), char.image.data, cmap='gray')
#    else:
#        for i, char in enumerate(chars):
#            imsave('%s%s_%d' % (folder, filename, i), char.image.data, cmap='gray')
