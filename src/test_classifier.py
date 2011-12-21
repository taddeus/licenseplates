#!/usr/bin/python
from cPickle import dump, load
from sys import argv, exit

from Classifier import Classifier

if len(argv) < 5:
    print 'Usage: python %s FILE_SUFFIX C GAMMA NEIGHBOURS' % argv[0]
    exit(1)

print 'Loading learning set'
learning_set = load(file('learning_set%s.dat' % argv[1], 'r'))

# Train the classifier with the learning set
classifier = Classifier(c=float(argv[1]), \
                        gamma=float(argv[2]), \
                        neighbours=int(argv[3]))
classifier.train(learning_set)

print 'Loading test set...'
test_set = load(file('test_set%s.dat' % argv[1], 'r'))
l = len(test_set)
matches = 0

for i, char in enumerate(test_set):
    prediction = classifier.classify(char, char.value)

    if char.value == prediction:
        print ':-----> Successfully recognized "%s"' % char.value,
        matches += 1
    else:
        print ':( Expected character "%s", got "%s"' \
                % (char.value, prediction),

    print '  --  %d of %d (%d%% done)' % (i + 1, l, int(100 * (i + 1) / l))

print '\n%d matches (%d%%), %d fails' % (matches, \
        int(100 * matches / l), \
        len(test_set) - matches)
