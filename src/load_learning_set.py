#!/usr/bin/python
from cPickle import dump, load
from sys import argv, exit

if len(argv) < 2:
    print 'Usage: python %s FILE_SUFFIX' % argv[0]
    exit(1)

print 'Loading characters...'
chars = load(file('characters%s.dat' % argv[1], 'r'))
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
print '\nTest set:', [c.value for c in test_set]
print '\nSaving learning set...'
dump(learning_set, file('learning_set%s.dat' % argv[1], 'w+'))
print 'Saving test set...'
dump(test_set, file('test_set%s.dat' % argv[1], 'w+'))
