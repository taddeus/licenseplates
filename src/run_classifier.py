#!/usr/bin/python
from sys import argv, exit
from pylab import subplot, imshow, show, axis, title
from math import sqrt, ceil

from create_characters import load_test_set
from create_classifier import load_classifier

if len(argv) < 3:
    print 'Usage: python %s NEIGHBOURS BLUR_SCALE [ C GAMMA ]' % argv[0]
    exit(1)

neighbours = int(argv[1])
blur_scale = float(argv[2])

# Load classifier
if len(argv) > 4:
    c = float(argv[3])
    gamma = float(argv[4])
    classifier = load_classifier(neighbours, blur_scale, c=c, gamma=gamma, \
            verbose=1)
else:
    classifier = load_classifier(neighbours, blur_scale, verbose=1)

# Load test set
test_set = load_test_set(neighbours, blur_scale, verbose=1)

# Classify each character in the test set, remembering all faulty
# classified characters
l = len(test_set)
matches = 0
classified = []

for i, char in enumerate(test_set):
    prediction = classifier.classify(char, char.value)

    if char.value != prediction:
        classified.append((char, prediction))

        print '"%s" was classified as "%s"' \
                % (char.value, prediction)
    else:
        matches += 1

    print '%d of %d (%d%% done)' % (i + 1, l, round(100 * (i + 1) / l))

print '\n%d matches (%.1f%%), %d fails' % (matches, \
        100.0 * matches / l, len(test_set) - matches)

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
