from svmutil import svm_model, svm_problem, svm_parameter, svm_predict, LINEAR
from cPicle import dump, load


class Classifier:
    def __init__(self, c=None, filename=None):
        if filename:
            # If a filename is given, load a modl from the fiven filename
            f = file(filename, 'r')
            self.model, self.param, self.character_map = load(f)
            f.close()
        else:
            self.param = svm_parameter()
            self.param.kernel_type = LINEAR
            self.param.C = c
            self.character_map = {}
            self.model = None

    def save(self, filename):
        """Save the SVM model in the given filename."""
        f = file(filename, 'w+')
        dump((self.model, self.param, self.character_map), f)
        f.close()

    def train(self, learning_set):
        """Train the classifier with a list of character objects that have
        known values."""
        classes = []
        features = []

        for char in learning_set:
            # Map the character to an integer for use in the SVM model
            if char.value not in self.character_map:
                self.character_map[char.value] = len(self.character_map)

            classes.append(self.character_map[char.value])
            features.append(char.get_feature_vector())

        problem = svm_problem(self.c, features)
        self.model = svm_model(problem, self.param)

        # Add prediction fucntion that returns a numeric class prediction
        self.model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

    def classify(self, character):
        """Classify a character object and assign its value."""
        prediction = self.model.predict(character.get_feature_vector())

        for value, svm_class in self.character_map.iteritems():
            if svm_class == prediction:
                return value
