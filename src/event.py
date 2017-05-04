
class Events(object):
    def __init__(self, num):
        self.current = 0
        self.eventsNumber = num
        self.events = []

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.events):
            raise StopIteration
        else:
            self.current += 1
            return self.events[self.current - 1]

    def addEvent(self):
        self.events.append(Event(len(self.events)))

    def get(self, idx):
        return self.events[idx]

    def getLast(self):
        return self.events[-1]


class Event(object):
    def __init__(self, idx):
        self.index = idx
        self.students = []
        self.features = []
        self.room = None
        self.timeslot = None

    def addStudent(self, student):
        self.students.append(student)

    def addFeature(self, feature):
        self.features.append(feature)

    def isInitialized(self):
        return self.room is not None and self.timeslot is not None
