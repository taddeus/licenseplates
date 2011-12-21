#!/usr/bin/python
import os
from sys import argv, exit

from Classifier import Classifier
from data import DATA_FOLDER, RESULTS_FOLDER
from create_characters import load_learning_set, load_test_set

if len(argv) < 3:
    print 'Usage: python %s NEIGHBOURS BLUR_SCALE' % argv[0]
    exit(1)

neighbours = int(argv[1])
blur_scale = float(argv[2])
suffix = '_%s_%s' % (blur_scale, neighbours)

if not os.path.exists(RESULTS_FOLDER):
    os.mkdir(RESULTS_FOLDER)

classifier_file = DATA_FOLDER + 'classifier%s.dat' % suffix
results_file = '%sresult%s.txt' % (RESULTS_FOLDER, suffix)

# Load learning set and test set
learning_set = load_learning_set(neighbours, blur_scale, verbose=1)
test_set = load_test_set(neighbours, blur_scale, verbose=1)

# Perform a grid-search to find the optimal values for C and gamma
C = [float(2 ** p) for p in xrange(-5, 16, 2)]
Y = [float(2 ** p) for p in xrange(-15, 4, 2)]

results = []
best = (0,)
i = 0

for c in C:
    for y in Y:
        classifier = Classifier(c=c, gamma=y, neighbours=neighbours, verbose=1)
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
