#!/usr/bin/python
from cPickle import load
from Classifier import Classifier

C = [float(2 ** p) for p in xrange(-5, 16, 2)]
Y = [float(2 ** p) for p in xrange(-15, 4, 2)]
best_classifier = None

print 'Loading learning set...'
learning_set = load(file('learning_set.dat', 'r'))
print 'Learning set:', [c.value for c in learning_set]
print 'Loading test set...'
test_set = load(file('test_set.dat', 'r'))
print 'Test set:', [c.value for c in test_set]

# Perform a grid-search on different combinations of soft margin and gamma
results = []
best = (0,)
i = 0

for c in C:
    for y in Y:
        classifier = Classifier(c=c, gamma=y)
        classifier.train(learning_set)
        result = classifier.test(test_set)

        if result > best[0]:
            best = (result, c, y, classifier)

        results.append(result)
        i += 1
        print '%d of %d, c = %f, gamma = %f, result = %d%%' \
              % (i, len(C) * len(Y), c, y, int(result * 100))

i = 0

print '\n     c\y',
for y in Y:
    print '| %f' % y,

print

for c in C:
    print ' %7s' % c,

    for y in Y:
        print '| %8d' % int(results[i] * 100),
        i += 1

    print

print '\nBest result: %.3f%% for C = %f and gamma = %f' % best[:3]

best[3].save('classifier.dat')
