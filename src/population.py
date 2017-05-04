from src.timetable import TimeTable


class Population(object):
    def __init__(self, events, rooms, features, students):
        self.events = events
        self.rooms = rooms
        self.features = features
        self.students = students
        self.populationSize = 100
        self.timeTables = []
        self.initPopulation()

    def initPopulation(self):
        for i in range(self.populationSize):
            t = TimeTable(self.events, self.rooms, self.features, self.students)
            t.init()
            self.timeTables.append(t)

