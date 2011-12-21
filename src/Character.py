from LocalBinaryPatternizer import LocalBinaryPatternizer as LBP

class Character:
    def __init__(self, value, corners, image, filename=None):
        self.value   = value
        self.corners = corners
        self.image   = image
        self.filename = filename

    def get_single_cell_feature_vector(self, neighbours=5):
        """Get the histogram of Local Binary Patterns over this entire
        image."""
        if hasattr(self, 'feature'):
            return

        pattern = LBP(self.image, neighbours=neighbours)
        self.feature = pattern.single_cell_features_vector()

    def get_feature_vector(self, cell_size=None):
        """Get the concatenated histograms of Local Binary Patterns. """
        pattern = LBP(self.image) if cell_size == None \
                  else LBP(self.image, cell_size)

        return pattern.create_features_vector()
