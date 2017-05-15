import copy
import numpy as np

from src.timetable import TimeTable


class Population(object):
    def __init__(self, events, rooms, features, students):
        self.events = events
        self.rooms = rooms
        self.features = features
        self.students = students
        self.populationSize = 100
        self.timeTables = []
        self.states = []
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
        for i in range(self.populationSize):
            t = TimeTable(self.events, self.rooms, self.features, self.students)
            t.reset()
            t.init()
            self.states.append(t.getState())
            self.timeTables.append(t)
            print 'Population', i + 1, 'of', self.populationSize, 'inited!'

    def mutation(self):
        for i in np.random.random_integers(0, self.populationSize - 1, size=self.populationSize / 5):
            self.timeTables[i].setState(self.states[i])
            self.timeTables[i].mutation()

    def randIterImprovement(self):
        for i in range(len(self.timeTables)):
            self.timeTables[i].setState(self.states[i])
            self.timeTables[i].randIterImprovement()
        self.setBest()
