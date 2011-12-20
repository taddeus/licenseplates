#!/usr/bin/python
from os import listdir
from os.path import exists
from cPickle import load, dump
from sys import argv, exit

from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from Character import Character
from Classifier import Classifier

if len(argv) < 3:
    print 'Usage: python %s NEIGHBOURS BLUR_SCALE' % argv[0]
    exit(1)

neighbours = int(argv[1])
blur_scale = float(argv[2])
suffix = '_%s_%s' % (blur_scale, neighbours)

chars_file = 'characters%s.dat' % suffix
learning_set_file = 'learning_set%s.dat' % suffix
test_set_file = 'test_set%s.dat' % suffix
classifier_file = 'classifier%s.dat' % suffix
results_file = 'results%s.txt' % suffix


# Load characters
if exists(chars_file):
    print 'Loading characters...'
    chars = load(open(chars_file, 'r'))
else:
    print 'Going to generate character objects...'
    chars = []

    for char in sorted(listdir('../images/LearningSet')):
        for image in sorted(listdir('../images/LearningSet/' + char)):
            f = '../images/LearningSet/' + char + '/' + image
            image = GrayscaleImage(f)
            norm = NormalizedCharacterImage(image, blur=blur_scale, height=42)
            #imshow(norm.data, cmap='gray'); show()
            character = Character(char, [], norm)
            character.get_single_cell_feature_vector(neighbours)
            chars.append(character)
            print char

    print 'Saving characters...'
    dump(chars, open(chars_file, 'w+'))


# Load learning set and test set
if exists(learning_set_file):
    print 'Loading learning set...'
    learning_set = load(open(learning_set_file, 'r'))
    print 'Learning set:', [c.value for c in learning_set]
    print 'Loading test set...'
    test_set = load(open(test_set_file, 'r'))
    print 'Test set:', [c.value for c in test_set]
else:
    print 'Going to generate learning set and test set...'
    learning_set = []
    test_set = []
    learned = []

    for char in chars:
        if learned.count(char.value) == 70:
            test_set.append(char)
        else:
            learning_set.append(char)
            learned.append(char.value)

    print 'Learning set:', [c.value for c in learning_set]
    print '\nTest set:', [c.value for c in test_set]
    print '\nSaving learning set...'
    dump(learning_set, file(learning_set_file, 'w+'))
    print 'Saving test set...'
    dump(test_set, file(test_set_file, 'w+'))


# Perform a grid-search to find the optimal values for C and gamma
C = [float(2 ** p) for p in xrange(-5, 16, 2)]
Y = [float(2 ** p) for p in xrange(-15, 4, 2)]

results = []
best = (0,)
i = 0

for c in C:
    for y in Y:
        classifier = Classifier(c=c, gamma=y, neighbours=neighbours)
        classifier.train(learning_set)
        result = classifier.test(test_set)

        if result > best[0]:
            best = (result, c, y, classifier)

        results.append(result)
        i += 1
        print '%d of %d, c = %f, gamma = %f, result = %d%%' \
              % (i, len(C) * len(Y), c, y, int(round(result * 100)))

i = 0
s = '     c\y'

for y in Y:
    s += ' | %f' % y

s += '\n'

for c in C:
    s += ' %7s' % c

    for y in Y:
        s +=  ' | %8d' % int(round(results[i] * 100))
        i += 1

    s += '\n'

s += '\nBest result: %.3f%% for C = %f and gamma = %f' \
        % ((best[0] * 100,) + best[1:3])

print 'Saving results...'
f = open(results_file, 'w+')
f.write(s + '\n')
f.close()

print 'Saving best classifier...'
best[3].save(classifier_file)

print '\n' + s
