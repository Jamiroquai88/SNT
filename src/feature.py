
class Features(object):
    def __init__(self, num):
        self.featuresNumber = num
        self.features = []

    def addFeature(self):
        self.features.append(Feature(len(self.features)))

    def get(self, idx):
        return self.features[idx]

    def getLast(self):
        return self.features[-1]


class Feature(object):
    def __init__(self, idx):
        self.index = idx
