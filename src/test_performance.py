#!/usr/bin/python
from cPickle import load
from sys import argv, exit
from time import time

from Classifier import Classifier

if len(argv) < 4:
    print 'Usage: python %s NEIGHBOURS BLUR_SCALE COUNT' % argv[0]
    exit(1)

neighbours = int(argv[1])
blur_scale = float(argv[2])
count = int(argv[3])
suffix = '_%s_%s' % (blur_scale, neighbours)

chars_file = 'characters%s.dat' % suffix
classifier_file = 'classifier%s.dat' % suffix

print 'Loading characters...'
chars = load(open(chars_file, 'r'))[:count]
count = len(chars)
print 'Read %d characters' % count

print 'Loading classifier...'
classifier = Classifier(filename=classifier_file)

start = time()

for char in chars:
    classifier.classify(char)

elapsed = time() - start
individual = elapsed / count

print 'Took %fs to classify %d caracters (%fms per character)' \
        % (elapsed, count, individual * 1000)
