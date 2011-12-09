#!/usr/bin/python
from pylab import subplot, show, imshow, axis
from cPickle import load

x, y = 25, 25
chars = load(file('chars', 'r'))[:(x * y)]

for i in range(x):
    for j in range(y):
        index = j * x + i
        subplot(x, y, index + 1)
        axis('off')
        imshow(chars[index].image.data, cmap='gray')

show()
