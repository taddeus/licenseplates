import os
from cPickle import load, dump


DATA_FOLDER = 'data/'
IMAGES_FOLDER = '../images/LearningSet/'
RESULTS_FOLDER = 'results/'


def assert_data_folder_exists():
    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)


def exists(filename):
    return os.path.exists(DATA_FOLDER + filename)


def fload(filename):
    f = open(DATA_FOLDER + filename, 'r')
    l = load(f)
    f.close()

    return l


def fdump(obj, filename):
    assert_data_folder_exists()
    f = open(DATA_FOLDER + filename, 'w+')
    dump(obj, f)
    f.close()
