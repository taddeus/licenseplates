from svmutil import svm_train, svm_problem, svm_parameter, svm_predict, \
        svm_save_model, svm_load_model
from cPickle import dump, load


class Classifier:
    def __init__(self, c=None, filename=None):
        if filename:
            # If a filename is given, load a modl from the fiven filename
            self.model = svm_load_model(filename + '-model')
            f = file(filename + '-characters', 'r')
            self.character_map = load(f)
            f.close()
        else:
            self.param = svm_parameter()
            self.param.kernel_type = 2
            self.param.C = c
            self.character_map = {}
            self.model = None

    def save(self, filename):
        """Save the SVM model in the given filename."""
        svm_save_model(filename + '-model', self.model)
        f = file(filename + '-characters', 'w+')
        dump(self.character_map, f)
        f.close()

    def train(self, learning_set):
        """Train the classifier with a list of character objects that have
        known values."""
        classes = []
        features = []
        l = len(learning_set)

        for i, char in enumerate(learning_set):
            print 'Training "%s"  --  %d of %d (%d%% done)' \
                    % (char.value, i + 1, l, int(100 * (i + 1) / l))
            # Map the character to an integer for use in the SVM model
            if char.value not in self.character_map:
                self.character_map[char.value] = len(self.character_map)

            classes.append(self.character_map[char.value])
            features.append(char.get_feature_vector())

        problem = svm_problem(classes, features)
        self.model = svm_train(problem, self.param)

    def classify(self, character):
        """Classify a character object and assign its value."""
        predict = lambda x: svm_predict([0], [x], self.model)[0][0]
        prediction = predict(character.get_feature_vector())

        for value, svm_class in self.character_map.iteritems():
            if svm_class == prediction:
                return value
