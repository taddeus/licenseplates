#!/usr/bin/python
from xml_helper_functions import xml_to_LicensePlate
from Classifier import Classifier
from cPickle import dump, load

chars = []

for i in range(9):
    for j in range(100):
        try:
            filename = '%04d/00991_%04d%02d' % (i, i, j)
            print 'loading file "%s"' % filename

            # is nog steeds een licensePlate object, maar die is nu heel anders :P
            plate = xml_to_LicensePlate(filename) 

            if hasattr(plate, 'characters'):
                chars.extend(plate.characters)
        except:
            print 'epic fail'

print 'loaded %d chars' % len(chars)

dump(chars, file('chars', 'w+'))
#----------------------------------------------------------------
chars = load(file('chars', 'r'))[:500]
learned = []
learning_set = []
test_set = []

for char in chars:
    if learned.count(char.value) > 12:
        test_set.append(char)
    else:
        learning_set.append(char)
        learned.append(char.value)

#print 'Learning set:', [c.value for c in learning_set]
#print 'Test set:', [c.value for c in test_set]
dump(learning_set, file('learning_set', 'w+'))
dump(test_set, file('test_set', 'w+'))
#----------------------------------------------------------------
learning_set = load(file('learning_set', 'r'))

# Train the classifier with the learning set
classifier = Classifier(c=30)
classifier.train(learning_set)
classifier.save('classifier')
#----------------------------------------------------------------
classifier = Classifier(filename='classifier')
test_set = load(file('test_set', 'r'))
l = len(test_set)
matches = 0

for i, char in enumerate(test_set):
    prediction = classifier.classify(char)

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
