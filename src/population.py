import numpy as np

from src.timetable import TimeTable

from src.user_exceptions import PopulationException


class Population(object):
    def __init__(self, events, rooms, features, students):
        self.events = events
        self.rooms = rooms
        self.features = features
        self.students = students
        self.populationSize = 2
        self.timeTables = []
        self.bestSolution = None

        self.initPopulation()
        self.mutation()
        self.randIterImprovement()

    def getBest(self):
        return self.timeTables[self.bestSolution].bestSolutionObject

    def initPopulation(self):
        for i in range(self.populationSize):
            t = TimeTable(self.events, self.rooms, self.features, self.students)
            t.init()
            self.timeTables.append(t)
        print 'Population inited, size:', self.populationSize

    def mutation(self):
        for i in np.random.random_integers(0, self.populationSize - 1, size=self.populationSize / 5):
            self.timeTables[i].mutation()

    def randIterImprovement(self):
        for x in self.timeTables:
            x.randIterImprovement()
        sol_list = []
        for x in self.timeTables:
            x.events = x.bestSolutionObject
            sol_list.append(x.solutionValue())
            print 'Value of timetable', x.solutionValue()
        self.bestSolution = min(sol_list)
