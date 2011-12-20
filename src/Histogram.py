class Histogram:

    def __init__(self, bins, min, max):
        self.bins = [0] * bins
        self.min = min
        self.max = max

    def add(self, number):
        #bin_index = self.get_bin_index(number)
        #self.bins[bin_index] += 1
        self.bins[number] += 1

    def remove(self, number):
        #bin_index = self.get_bin_index(number)
        #self.bins[bin_index] -= 1
        self.bins[number] -= 1

    def get_bin_index(self, number):
        return (number - self.min) / ((self.max - self.min) / len(self.bins))

    def normalize(self):
        minimum = min(self.bins)
        self.bins = map(lambda b: b - minimum, self.bins)
        maximum = float(max(self.bins))
        self.bins = map(lambda b: b / maximum, self.bins)

    def intersect(self, other):
        h1 = self.bins
        h2 = other.bins

        match = 0

        # Add the minimum of each bin to the result
        for b in xrange(len(self.bins)):
            match += min(h1[b], h2[b])

        # Normalize by dividing by the number of pixels
        return float(match) / sum(h2)
