#!/usr/bin/python
from matplotlib.pyplot import imshow, subplot, show
from LocalBinaryPatternizer import LocalBinaryPatternizer
from GrayscaleImage import GrayscaleImage
from cPickle import load
from numpy import zeros, resize

chars = load(file('characters.dat', 'r'))[::2]
left = None
right = None

s = {}

for char in chars:
    if char.value not in s:
        s[char.value] = [char]
    else:
        s[char.value].append(char)

left = s['F'][2].image
right = s['A'][0].image

size = 12

d = (left.size[0] * 4, left.size[1] * 4)
#GrayscaleImage.resize(left, d)
#GrayscaleImage.resize(right, d)

p1 = LocalBinaryPatternizer(left, size)
h1 = p1.get_single_histogram()
p1.create_features_vector()
p1 = p1.features

p2 = LocalBinaryPatternizer(right, size)
h2 = p2.get_single_histogram()
p2.create_features_vector()
p2 = p2.features

total_intersect = h1.intersect(h2)

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
print 'Single histogram instersection: %d%%' % int(total_intersect * 100)

subplot(311)
imshow(left.data, cmap='gray')
subplot(312)
imshow(match, cmap='gray')
subplot(313)
imshow(right.data, cmap='gray')

show()
