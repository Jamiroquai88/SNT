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
        self.dailySlots = 9
        self.days = self.timeslots / self.dailySlots
        self.findFeasibleIters = 1000

    def init(self):
        print 'Initialiazing population ...'
        while True:
            if self.isFeasible():
                print 'IS FEASIBLE!!!'
                return True
            else:
                # print 'Is not feasible!'
                # while True:
                self.events.initTimeslots(self.timeslots)
                self.events.initRooms(self.timeslots, self.rooms)
                self.events.localSearch(self)
                return True

    def mutation(self):
        n = self.events.eventsNumber
        for i in np.random.random_integers(0, n - 1, size=n / 5):
            self.findEarliestFeasible(self.events.get(i))

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

    def isFeasible(self, e=None):
        if e:
            return self.hardConstraint1(e) and self.hardConstraint2(e) \
                   and self.hardConstraint3(e) and self.hardConstraint4(e)
        else:
            return self.hardConstraint1() and self.hardConstraint2() \
                   and self.hardConstraint3() and self.hardConstraint4()

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

    def solutionValue(self):
        return self.softConstraint1() + self.softConstraint2() + self.softConstraint3()

    def softConstraint1(self):
        """ Count the number of occurences of a student having just one class on a day 
            (e.g. count 2 if a student has two days with only one class).
            
        """
        summ = 0
        for s in self.students:
            for day in range(self.days):
                daily_sum = 0
                for t in range(self.dailySlots):
                    for e in self.events.getByTimeslot(day * self.dailySlots + t):
                        if s in e.students:
                            daily_sum += 1
                if daily_sum == 1:
                    summ += 1
        return summ

    def softConstraint2(self):
        """ Count the number of occurrences of a student having more than two classes consecutively
            (3 consecutively scores 1, 4 consecutively scores 2, 5 consecutively scores 3, etc), classes at the end
            of the day followed by classes at the beginning of the next day do not count as consecutive.
          
        """
        summ = 0
        for s in self.students:
            for day in range(self.days):
                cons_max = 0
                cons = 0
                for t in range(self.dailySlots):
                    for e in self.events.getByTimeslot(day * self.dailySlots + t):
                        if s in e.students:
                            cons += 1
                            if cons > cons_max:
                                cons_max = cons
                        else:
                            cons = 0
                if cons_max > 2:
                    summ += cons_max - 2
        return summ

    def softConstraint3(self):
        """ Count the number of occurrences of a student having a class in the last timeslot of the day.
        
        """
        summ = 0
        for s in self.students:
            for day in range(self.days):
                if s in self.events.getByTimeslot(day * self.dailySlots + self.dailySlots - 1):
                    summ += 1
        return summ

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

    def findEarliestFeasible(self, event):
        old_t = event.timeslot
        old_r = event.room
        for t in range(self.timeslots):
            for r in self.rooms.sortBySize():
                event.timeslot = t
                event.r = r
                if self.isFeasible(event):
                    return
                else:
                    event.timeslot = old_t
                    event.room = old_r



