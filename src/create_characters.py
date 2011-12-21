#!/usr/bin/python
from os import listdir

from GrayscaleImage import GrayscaleImage
from NormalizedCharacterImage import NormalizedCharacterImage
from Character import Character
from data import IMAGES_FOLDER, exists, fload, fdump


NORMALIZED_HEIGHT = 42


def load_characters(neighbours, blur_scale, verbose=0):
    chars_file = 'characters_%s_%s.dat' % (blur_scale, neighbours)

    if exists(chars_file):
        print 'Loading characters...'
        chars = fload(chars_file)
    else:
        print 'Going to generate character objects...'
        chars = []

        for char in sorted(listdir(IMAGES_FOLDER)):
            count = 0

            for image in sorted(listdir(IMAGES_FOLDER + char)):
                image = GrayscaleImage(IMAGES_FOLDER + char + '/' + image)
                norm = NormalizedCharacterImage(image, blur=blur_scale, \
                                                height=NORMALIZED_HEIGHT)
                character = Character(char, [], norm)
                character.get_single_cell_feature_vector(neighbours)
                chars.append(character)

                count += 1

                if verbose:
                    print 'Loaded character %s %d times' % (char, count)

        if verbose:
            print 'Saving characters...'

        fdump(chars, chars_file)

    return chars


def load_learning_set(neighbours, blur_scale, verbose=0):
    learning_set_file = 'learning_set_%s_%s.dat' % (blur_scale, neighbours)

    if exists(learning_set_file):
        if verbose:
            print 'Loading learning set...'

        learning_set = fload(learning_set_file)

        if verbose:
            print 'Learning set:', [c.value for c in learning_set]
    else:
        learning_set = generate_sets(neighbours, blur_scale, \
                verbose=verbose)[0]

    return learning_set


def load_test_set(neighbours, blur_scale, verbose=0):
    test_set_file = 'test_set_%s_%s.dat' % (blur_scale, neighbours)

    if exists(test_set_file):
        if verbose:
            print 'Loading test set...'

        test_set = fload(test_set_file)

        if verbose:
            print 'Test set:', [c.value for c in test_set]
    else:
        test_set = generate_sets(neighbours, blur_scale, verbose=verbose)[1]

    return test_set


def generate_sets(neighbours, blur_scale, verbose=0):
    suffix = '_%s_%s' % (blur_scale, neighbours)
    learning_set_file = 'learning_set%s.dat' % suffix
    test_set_file = 'test_set%s.dat' % suffix

    chars = load_characters(neighbours, blur_scale, verbose=verbose)

    if verbose:
        print 'Going to generate learning set and test set...'

    learning_set = []
    test_set = []
    learned = []

    for char in chars:
        if learned.count(char.value) == 70:
            test_set.append(char)
        else:
            learning_set.append(char)
            learned.append(char.value)

    if verbose:
        print 'Learning set:', [c.value for c in learning_set]
        print '\nTest set:', [c.value for c in test_set]
        print '\nSaving learning set...'

    fdump(learning_set, learning_set_file)

    if verbose:
        print 'Saving test set...'

    fdump(test_set, test_set_file)

    return learning_set, test_set


if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 3:
        print 'Usage: python %s NEIGHBOURS BLUR_SCALE' % argv[0]
        exit(1)

    neighbours = int(argv[1])
    blur_scale = float(argv[2])

    # Generate the character file and the learning set/test set files
    load_learning_set(neighbours, blur_scale, verbose=1)
    load_test_set(neighbours, blur_scale, verbose=1)
