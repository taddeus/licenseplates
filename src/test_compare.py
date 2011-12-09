#!/usr/bin/python
from matplotlib.pyplot import imshow, subplot, show
from LocalBinaryPatternizer import LocalBinaryPatternizer
from GrayscaleImage import GrayscaleImage
from cPickle import load
from numpy import zeros, resize

chars = load(file('chars', 'r'))[::2]
left = None
right = None

for c in chars:
    if c.value == '8':
        if left == None:
            left = c.image
        elif right == None:
            right = c.image
        else:
            break

size = 16

d = (left.size[0] * 4, left.size[1] * 4)
#GrayscaleImage.resize(left, d)
#GrayscaleImage.resize(right, d)

p1 = LocalBinaryPatternizer(left, size)
p1.create_features_vector()
p1 = p1.features
p2 = LocalBinaryPatternizer(right, size)
p2.create_features_vector()
p2 = p2.features

s = (len(p1), len(p1[0]))
match = zeros(left.shape)
m = 0

for y in range(s[0]):
    for x in range(s[1]):
        h1 = p1[y][x]
        h2 = p2[y][x]
        intersect = h1.intersect(h2)
        print intersect

        for i in xrange(size):
            for j in xrange(size):
                try:
                    match[y*size + i, x*size + j] = 1 - intersect
                except IndexError:
                    pass

        m += intersect

print 'Match: %d%%' % int(m / (s[0] * s[1]) * 100)

subplot(311)
imshow(left.data, cmap='gray')
subplot(312)
imshow(match, cmap='gray')
subplot(313)
imshow(right.data, cmap='gray')

show()
