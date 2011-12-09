#!/usr/bin/python
from pylab import subplot, show, imshow, axis
from cPickle import load

chars = filter(lambda c: c.value == 'A', load(file('chars', 'r')))

for i in range(10):
    for j in range(3):
        index = j * 10 + i
        subplot(10, 3, index + 1)
        axis('off')
        imshow(chars[index].image.data, cmap='gray')

show()
