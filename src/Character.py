from LocalBinaryPatternizer import LocalBinaryPatternizer as LBP

class Character:
    def __init__(self, value, corners, image, filename=None):
        self.value   = value
        self.corners = corners
        self.image   = image
        self.filename = filename

    def get_single_cell_feature_vector(self):
        if hasattr(self, 'feature'):
            return

        self.feature = LBP(self.image).single_cell_features_vector()

    def get_feature_vector(self, cell_size=None):
        pattern = LBP(self.image) if cell_size == None \
                  else LBP(self.image, cell_size)

        return pattern.create_features_vector()
