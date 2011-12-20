#!/usr/bin/python
from xml_helper_functions import xml_to_LicensePlate
from Classifier import Classifier
from cPickle import dump, load

chars = load(file('characters.dat', 'r'))
learning_set = []
test_set = []

#s = {}
#
#for char in chars:
#    if char.value not in s:
#        s[char.value] = [char]
#    else:
#        s[char.value].append(char)
#
#for value, chars in s.iteritems():
#    learning_set += chars[::2]
#    test_set += chars[1::2]

learned = []

for char in chars:
    if learned.count(char.value) == 70:
        test_set.append(char)
    else:
        learning_set.append(char)
        learned.append(char.value)

print 'Learning set:', [c.value for c in learning_set]
print 'Test set:', [c.value for c in test_set]
print 'Saving learning set...'
dump(learning_set, file('learning_set.dat', 'w+'))
print 'Saving test set...'
dump(test_set, file('test_set.dat', 'w+'))
#----------------------------------------------------------------
print 'Loading learning set'
learning_set = load(file('learning_set.dat', 'r'))

# Train the classifier with the learning set
classifier = Classifier(c=512, gamma=.125, cell_size=12)
classifier.train(learning_set)
classifier.save('classifier.dat')
print 'Saved classifier'
#----------------------------------------------------------------
print 'Loading classifier'
classifier = Classifier(filename='classifier.dat')
print 'Loading test set'
test_set = load(file('test_set.dat', 'r'))
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
        int(100 * matches / len(test_set)), \
        len(test_set) - matches)
