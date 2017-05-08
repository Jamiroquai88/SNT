import numpy as np

from src.timetable import TimeTable

from src.user_exceptions import PopulationException


class Population(object):
    def __init__(self, events, rooms, features, students):
        self.events = events
        self.rooms = rooms
        self.features = features
        self.students = students
        self.populationSize = 100
        self.timeTables = []
        self.bestSolution = None

        self.initPopulation()
        self.mutation()
        self.localSearch()

    def getBest(self):
        sol = self.timeTables[self.bestSolution].events
        if self.timeTables[self.bestSolution].isFeasible():
            return sol
        else:
            raise PopulationException(
                '[getBest] Solution is not feasible!'
            )

    def initPopulation(self):
        for i in range(self.populationSize):
            t = TimeTable(self.events, self.rooms, self.features, self.students)
            t.init()
            self.timeTables.append(t)
        print 'Population inited, size:', self.populationSize

    def mutation(self):
        for i in np.random.random_integers(0, self.populationSize - 1, size=self.populationSize / 5):
            self.timeTables[i].mutation()

    def localSearch(self):
        sol_list = []
        for x in self.timeTables:
            sol_list.append(x.solutionValue())
        self.bestSolution = min(sol_list)
