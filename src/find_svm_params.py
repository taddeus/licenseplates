C = [2 ** p for p in xrange(-5, 16, 2)]:
Y = [2 ** p for p in xrange(-15, 4, 2)]
best_result = 0
best_classifier = None

learning_set = load(file('learning_set', 'r'))
test_set = load(file('test_set', 'r'))

# Perform a grid-search on different combinations of soft margin and gamma
for c in C:
    for y in Y:
        classifier = Classifier(c=c, gamma=y)
        classifier.train(learning_set)
        result = classifier.test(test_set)

        if result > best_result:
            best_classifier = classifier

        print 'c = %f, gamma = %f, result = %d%%' % (c, y, int(result * 100))

best_classifier.save('best_classifier')
