import random
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
        self.mutation()

    def initPopulation(self):
        for i in range(self.populationSize):
            t = TimeTable(self.events, self.rooms, self.features, self.students)
            t.init()
            self.timeTables.append(t)
        print 'Population inited, size:', self.populationSize

    def mutation(self):
        for i in range(self.populationSize):
            if random.uniform(0, 1) < 0.2:
                self.timeTables[i].mutation()

