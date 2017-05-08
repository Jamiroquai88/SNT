
class Rooms(object):
    def __init__(self, num):
        self.roomsNumber = num
        self.rooms = []

    def __iter__(self):
        current = 0
        while current < len(self.rooms):
            yield self.rooms[current]
            current += 1

    def addRoom(self, size):
        self.rooms.append(Room(len(self.rooms), size))

    def get(self, idx):
        return self.rooms[idx]

    def getLast(self):
        return self.rooms[-1]

    def sortBySize(self):
        return sorted(self.rooms, key=lambda x: x.size)


class Room(object):
    def __init__(self, idx, size):
        self.index = idx
        self.size = size
        self.features = []

    def addFeature(self, feature):
        self.features.append(feature)