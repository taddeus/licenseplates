from LocalBinaryPatternizer import LocalBinaryPatternizer

class Character:
    def __init__(self, value, corners, image, filename=None):
        self.value   = value
        self.corners = corners
        self.image   = image
        self.filename = filename

    def get_feature_vector(self):
        pattern = LocalBinaryPatternizer(self.image)

        return pattern.create_features_vector()
