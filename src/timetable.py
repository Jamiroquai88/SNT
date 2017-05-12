import random
import itertools
import numpy as np

from src.parser import TIMParser

from src.user_exceptions import TimeTableException


class TimeTable(object):
    def __init__(self, events, rooms, features, students):
        self.events = events
        self.rooms = rooms
        self.features = features
        self.students = students
        self.bestSolution = float('inf')
        self.bestSolutionObject = None
        self.timeslots = 45
        self.dailySlots = 9
        self.days = self.timeslots / self.dailySlots
        self.findFeasibleIters = 1000
        self.randIterImprovementIters = 20000

    def loadInitialSolution(self, f):
        with open(f) as fd:
            lines = fd.readlines()
        for i in range(len(lines)):
            t = int(lines[i].split()[0])
            r = self.rooms.getByIndex(int(lines[i].split()[1]))
            self.events[i].timeslot = t
            self.events[i].room = r



    def init(self):
        while True:
            if self.isFeasible():
                return True
            else:
                # print 'Is not feasible!'
                while True:
                    self.events.initTimeslots(self.timeslots)
                    self.events.initRooms(self.timeslots, self.rooms)
                    self.events.localSearch(self)
                    if self.isFeasible():
                        break
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

    def getRandEvent(self):
        return self.events.get((np.random.randint(0, self.events.eventsNumber)))

    def getRandTimeslot(self):
        return np.random.randint(0, self.timeslots)

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

    def solutionValue(self, e=None):
        if e is None:
            return self.softConstraint1() + self.softConstraint2() + self.softConstraint3()
        else:
            return self.softConstraint1(e) + self.softConstraint2(e) + self.softConstraint3(e)

    def softConstraint1(self, event=None):
        """ Count the number of occurences of a student having just one class on a day 
            (e.g. count 2 if a student has two days with only one class).
            
        """
        summ = 0
        if event is None:
            for s in self.students:
                for day in range(self.days):
                    daily_sum = 0
                    for t in range(self.dailySlots):
                        for e in self.events.getByTimeslot(day * self.dailySlots + t):
                            if s in e.students:
                                daily_sum += 1
                    if daily_sum == 1:
                        summ += 1
        else:
            for s in self.students:
                for day in range(self.days):
                    daily_sum = 0
                    for t in range(self.dailySlots):
                        for e in self.events.getByTimeslot(day * self.dailySlots + t):
                            if e == event and s in e.students:
                                daily_sum += 1
                    if daily_sum == 1:
                        summ += 1
        # print 'Penalty for students having single events on a day =', summ
        return summ

    def softConstraint2(self, event=None):
        """ Count the number of occurrences of a student having more than two classes consecutively
            (3 consecutively scores 1, 4 consecutively scores 2, 5 consecutively scores 3, etc), classes at the end
            of the day followed by classes at the beginning of the next day do not count as consecutive.
          
        """
        summ = 0
        if event is None:
            for s in self.students:
                for day in range(self.days):
                    cons_sum = 0
                    cons = 0
                    for t in range(self.dailySlots):
                        students = self.events.getStudentsBySlot(day * self.dailySlots + t)
                        if s in students:
                            cons += 1
                            if cons > 2:
                                cons_sum += 1
                        else:
                            cons = 0
                    summ += cons_sum
        else:
            for s in self.students:
                for day in range(self.days):
                    cons_sum = 0
                    cons = 0
                    for t in range(self.dailySlots):
                        students = self.events.getStudentsBySlot(day * self.dailySlots + t)
                        if s in students and s in event.students and event.timeslot == day * self.dailySlots + t:
                            cons += 1
                            if cons > 2:
                                print 'student', s.index, 'day', day, 'slot', day * self.dailySlots + t
                                cons_sum += 1
                        else:
                            cons = 0
        # print 'Penalty for students having three or more events in a row =', summ
        return summ

    def softConstraint3(self, event=None):
        """ Count the number of occurrences of a student having a class in the last timeslot of the day.
        
        """
        summ = 0
        if event is None:
            for day in range(self.days):
                for x in self.events.getByTimeslot(day * self.dailySlots + self.dailySlots - 1):
                    summ += len(x.students)
        else:
            for day in range(self.days):
                for x in self.events.getByTimeslot(day * self.dailySlots + self.dailySlots - 1):
                    if x == event:
                        summ += len(x.students)
        # print 'Penalty for students having end of day events =', summ
        return summ

    def findFeasible(self, event, hard=True):
        if self.isFeasible(event) and hard:
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

    def findFeasibleTimeslot(self, event):
        old_t = event.timeslot
        cnt = 0
        while True:
            cnt += 1
            event.timeslot = np.random.randint(0, self.timeslots)
            if self.isFeasible():
                return True
            if cnt > self.findFeasibleIters:
                event.timeslot = old_t
                return False

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

    def getState(self):
        states = []
        for e in self.events:
            states.append([e.timeslot, e.room.index])
        return states

    def setState(self, state):
        for i in range(len(state)):
            e = self.events.get(i)
            e.timeslot, e.room = state[i][0], self.rooms.get(state[i][1])

    def randIterImprovement(self):
        sol = self.solutionValue()
        self.bestSolution = sol
        self.bestSolutionObject = self.getState()
        for i in range(self.randIterImprovementIters):
            print 'Random iteration improvement, iteration:', i, 'from', self.randIterImprovementIters
            tmp_state = self.getState()
            tmp_sol_dict = {}
            tmp_obj_dict = {}
            for j in range(11):
                self.setState(tmp_state)
                if j == 0:
                    val = self.N1()
                elif j == 1:
                    val = self.N2()
                elif j == 2:
                    val = self.N3()
                elif j == 3:
                    val = self.N4()
                elif j == 4:
                    val = self.N5()
                elif j == 5:
                    val = self.N6()
                elif j == 6:
                    val = self.N7()
                elif j == 7:
                    val = self.N8()
                elif j == 8:
                    val = self.N9()
                elif j == 9:
                    val = self.N10()
                elif j == 10:
                    val = self.N11()
                else:
                    raise TimeTableException(
                        '[randIterImprovement] Unexpected method!'
                    )
                tmp_sol_dict[val] = j
                tmp_obj_dict[val] = self.getState()
            sol_star = min(tmp_sol_dict.keys())
            if sol_star < self.bestSolution:
                self.bestSolution = sol_star
                self.bestSolutionObject = tmp_obj_dict[sol_star]
                self.setState(self.bestSolutionObject)
                if sol_star == 0:
                    TIMParser.dumpOutput('datasets/example_02.sln', self.bestSolutionObject)
                    return 0
                sol = sol_star
            else:
                delta = sol_star - sol
                if random.uniform(0, 1) < np.exp(-delta):
                    self.setState(tmp_obj_dict[sol_star])
                    sol = sol_star
                else:
                    self.setState(self.bestSolutionObject)
            print 'Value of this solution', self.solutionValue()
            print '===================================================================================================='

    def N1(self):
        """ Select two courses at random and swap timeslots. 

        """
        # print 'Executing N1'
        e1 = self.getRandEvent()
        e2 = self.getRandEvent()
        e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
        if not self.isFeasible():
            e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
        return self.solutionValue()

    def N2(self):
        """ Choose a single course at random and move to a new random feasible timeslot. 

        """
        # print 'Executing N2'
        e = self.getRandEvent()
        et = e.timeslot
        if not self.findFeasibleTimeslot(e):
            e.timeslot = et
        return self.solutionValue()

    def N3(self):
        """ Select two timeslots at random and simply swap all the courses in
            one timeslot with all the courses in the other timeslot. 

        """
        # print 'Executing N3'
        t1 = self.getRandTimeslot()
        t2 = self.getRandTimeslot()
        e1 = self.events.getByTimeslot(t1)
        e2 = self.events.getByTimeslot(t2)
        for e in e1:
            e.timeslot = t2
        for e in e2:
            e.timeslot = t1
        if not self.isFeasible():
            for e in e1:
                e.timeslot = t1
            for e in e2:
                e.timeslot = t2
        return self.solutionValue()

    def N4(self):
        """ Take 2 timeslots (selected at random), say ti and tj (where j>i) where
            the timeslots are ordered t1, t2, ... t45. Take all the exams in ti and
            allocate them to tj. Now take the exams that were in tj and allocate
            them to tj-1. Then allocate those that were in tj-1 to tj-2 and so on until
            we allocate those that were in ti+1 to ti and terminate the process. 

        """
        state = self.getState()
        while True:
            t1 = self.getRandTimeslot()
            t2 = self.getRandTimeslot()
            if t1 == t2:
                continue
            else:
                j = max([t1, t2])
                i = min([t1, t2])
                for x in self.events.getByTimeslot(j):
                    x.timeslot = i
                while i < j:
                    for x in self.events.getByTimeslot(j - 1):
                        x.timeslot = j
                    j -= 1
            if self.isFeasible():
                return self.solutionValue()
            else:
                self.setState(state)
                return self.solutionValue()

    def N5(self):
        """ Move the highest penalty course from a random 10% selection of the
            courses to a random feasible timeslot. 

        """
        # val_dict = {}
        # for e in self.events:
        #     val_dict[self.solutionValue(e)] = e
        # self.findFeasible(val_dict[max(val_dict.keys())], hard=False)
        # return self.solutionValue()
        return float('inf')

    def N6(self):
        """ Carry out the same process as in N5 but with 20% of the courses. 

        """
        # n = self.events.eventsNumber
        # for i in np.random.random_integers(0, n - 1, size=n / 5):
        #     self.N5()
        # return self.solutionValue()
        return float('inf')

    def N7(self):
        """ Move the highest penalty course from a random 10% selection of the
            courses to a new feasible timeslot which can generate the lowest
            penalty cost. 

        """
        # while True:
        #     val_dict = {}
        #     for e in self.events:
        #         val_dict[self.solutionValue(e)] = e
        #     e1 = val_dict[max(val_dict.keys())]
        #     e2 = val_dict[min(val_dict.keys())]
        #     e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
        #     if self.isFeasible():
        #         return self.solutionValue()
        #     else:
        #         e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
        #         return max(val_dict.keys())
        return float('inf')

    def N8(self):
        """ Carry out the same process as in N7 but with 20% of the courses.

        """
        # print 'Executing N8'
        # n = self.events.eventsNumber
        # for i in np.random.random_integers(0, n - 1, size=n / 5):
        #     self.N7()
        # return self.solutionValue()
        return float('inf')

    def N9(self):
        """ Select one course at random, select a timeslot at random (distinct
            from the one that was assigned to the selected course) and then
            apply the kempe chain from Thompson and Dowsland (1996).

        """
        # print 'Executing N9'
        # return self.solutionValue()
        return float('inf')

    def N10(self):
        """ This is the same as N9 except the highest penalty course from 5%
            selection of the courses is selected at random. 

        """
        # print 'Executing N10'
        # return self.solutionValue()
        return float('inf')

    def N11(self):
        """ Carry out the same process as in N9 but with 20% of the courses. 

        """
        # print 'Executing N11'
        # n = self.events.eventsNumber
        # for i in np.random.random_integers(0, n - 1, size=n / 5):
        #     self.N9()
        # return self.solutionValue()
        return float('inf')