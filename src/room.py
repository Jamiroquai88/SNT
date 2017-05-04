
class Rooms(object):
    def __init__(self, num):
        self.roomsNumber = num
        self.rooms = []

    def addRoom(self, size):
        self.rooms.append(Room(len(self.rooms), size))

    def get(self, idx):
        return self.rooms[idx]

    def getLast(self):
        return self.rooms[-1]


class Room(object):
    def __init__(self, idx, size):
        self.index = idx
        self.size = size
        self.features = []

    def addFeature(self, feature):
        self.features.append(feature)