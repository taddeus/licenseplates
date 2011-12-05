class Histogram:

    def __init__(self, bins, min, max):
        self.bins = [0] * bins
        self.min = min
        self.max = max

    def add(self, number):
        bin_index = self.get_bin_index(number)
        self.bins[bin_index] += 1

    def remove(self, number):
        bin_index = self.get_bin_index(number)
        self.bins[bin_index] -= 1

    def get_bin_index(self, number):
        return (number - self.min) / ((self.max - self.min) / len(self.bins))

