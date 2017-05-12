import numpy as np

from src.timetable import TimeTable


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
        if self.bestSolution is None:
            self.setBest()
        return self.timeTables[self.bestSolution].bestSolutionObject

    def setBest(self):
        sol_list = []
        for x in self.timeTables:
            x.setState(x.bestSolutionObject)
            sol_list.append(x.solutionValue())
        self.bestSolution = sol_list.index(min(sol_list))

    def initPopulation(self):
        t1 = TimeTable(self.events, self.rooms, self.features, self.students)
        t1.loadInitialSolution('solutions/small_1__1.sln')
        self.timeTables.append(t1)
        t2 = TimeTable(self.events, self.rooms, self.features, self.students)
        t2.loadInitialSolution('solutions/small_1__2.sln')
        self.timeTables.append(t2)
        # for i in range(self.populationSize):
        #     t = TimeTable(self.events, self.rooms, self.features, self.students)
        #     t.init()
        #     self.timeTables.append(t)
        print 'Population inited, size:', self.populationSize

    def mutation(self):
        for i in np.random.random_integers(0, self.populationSize - 1, size=self.populationSize / 5):
            self.timeTables[i].mutation()

    def randIterImprovement(self):
        for x in self.timeTables:
            x.randIterImprovement()
        self.setBest()
