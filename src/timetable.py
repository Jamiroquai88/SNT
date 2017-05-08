import sys
import random
import itertools
import numpy as np


class TimeTable(object):
    def __init__(self, events, rooms, features, students):
        self.events = events
        self.rooms = rooms
        self.features = features
        self.students = students
        self.timeslots = 45
        self.findFeasibleIters = 1000

    def init(self):
        print 'Initialiazing population ...'
        while True:
            if self.isFeasible():
                print 'IS FEASIBLE!!!'
                return True
            else:
                print 'Is not feasible!'
                while True:
                    self.events.initTimeslots(self.timeslots)
                    self.events.initRooms(self.timeslots, self.rooms)
                    if self.events.localSearch(self):
                        break

    def mutation(self):
        for e in self.events:
            if random.uniform(0, 1) < 0.2:
                self.events.mutation()

    def isFeasible(self, e=None):
        if e:
            return self.hardConstraint1(e) and self.hardConstraint2(e) \
                   and self.hardConstraint3(e) and self.hardConstraint4(e)
        else:
            return self.hardConstraint1() and self.hardConstraint2() \
                   and self.hardConstraint3() and self.hardConstraint4()

    def getFeasibles(self):
        a = []
        for x in self.events:
            if self.isFeasible(x):
                a.append(x)
        return a

    def getUnfeasibles(self):
        a = []
        for x in self.events:
            if not self.isFeasible(x):
                a.append(x)
        return a

    def hardConstraint1(self, event=None):
        """ No student can be assigned to more than one course at the same time.

        """
        if event is not None:
            if event.isInitialized():
                for x in self.events:
                    if x.isInitialized() and x != event:
                        if x.timeslot == event.timeslot and bool(set(x.students).intersection(event.students)):
                            return False
            else:
                return False
        else:
            for x, y in itertools.combinations(self.events, 2):
                if x.isInitialized() and y.isInitialized():
                    if x.timeslot == y.timeslot and bool(set(x.students).intersection(y.students)):
                        return False
                else:
                    return False
        return True

    def hardConstraint2(self, event=None):
        """ The room should satisfy the features required by the course.

        """
        if event is not None:
            if event.isInitialized():
                if not set(event.features).issubset(event.room.features):
                    return False
            else:
                return False
        else:
            for x in self.events:
                if x.isInitialized():
                    if not set(x.features).issubset(x.room.features):
                        return False
                else:
                    return False
        return True

    def hardConstraint3(self, event=None):
        """ The number of students attending the course should be less than or equal to the capacity of the room.

        """
        if event is not None:
            if event.isInitialized():
                if event.room.size < len(event.students):
                    return False
            else:
                return False
        else:
            for x in self.events:
                if x.isInitialized():
                    if x.room.size < len(x.students):
                        return False
                else:
                    return False
        return True

    def hardConstraint4(self, event=None):
        """ No more than one course is allowed at a timeslot in each room.

        """
        if event is not None:
            if event.isInitialized():
                for x in self.events.getByTimeslot(event.timeslot):
                    if x.isInitialized():
                        if x != event:
                            if x.timeslot == event.timeslot and x.room == event.room:
                                return False
                    else:
                        return False
            else:
                return False
        else:
            for x, y in itertools.combinations(self.events, 2):
                if x.isInitialized() and y.isInitialized():
                    if x.timeslot == y.timeslot and x.room == y.room:
                        return False
                else:
                    return False
        return True

    def findFeasible(self, event):
        if self.isFeasible(event):
            return True
        old_t = event.timeslot
        old_r = event.room
        before = len(self.getFeasibles())
        cnt = 0
        while True:
            cnt += 1
            event.timeslot = np.random.randint(0, self.timeslots)
            event.room = self.rooms.get(np.random.randint(0, self.rooms.roomsNumber))
            if self.isFeasible(event) and before < len(self.getFeasibles()):
                break
            else:
                if cnt > self.findFeasibleIters:
                    event.timeslot = old_t
                    event.room = old_r
                    return False
        return True
