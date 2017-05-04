import numpy as np


class TimeTable(object):
    def __init__(self, events, rooms, features, students):
        self.events = events
        self.rooms = rooms
        self.features = features
        self.students = students
        self.timeslots = 45

    def init(self):
        print 'Initialiazing population ...'
        while True:
            if self.isFeasible():
                break
            else:
                print 'Is not feasible!'
                for x in self.events:
                    x.timeslot = np.random.randint(0, 45)
                    x.room = self.rooms.get(np.random.randint(0, self.rooms.roomsNumber))

    def isFeasible(self):
        return self.hardConstraint1() and self.hardConstraint2() and self.hardConstraint3() and self.hardConstraint4()

    def hardConstraint1(self):
        """ No student can be assigned to more than one course at the same time.
        
        """
        print 'Checking hardConstraint1 ...'
        for s in self.students:
            for x in self.events:
                for y in self.events:
                    if x != y:
                        if x.isInitialized() and y.isInitialized():
                            if s in x.students and s in y.students and x.timeslot == y.timeslot:
                                return False
                        else:
                            return False
        return True

    def hardConstraint2(self):
        """ The room should satisfy the features required by the course.
        
        """
        print 'Checking hardConstraint2 ...'
        for x in self.events:
            if x.isInitialized():
                if not set(x.room.features).issubset(x.features):
                    return False
            else:
                return False
        return True

    def hardConstraint3(self):
        """ The number of students attending the course should be less than or equal to the capacity of the room.
        
        """
        print 'Checking hardConstraint3 ...'
        for x in self.events:
            if x.isInitialized():
                if x.room.size > len(x.students):
                    return False
            else:
                return False
        return True

    def hardConstraint4(self):
        """ No more than one course is allowed at a timeslot in each room.
        
        """
        print 'Checking hardConstraint4 ...'
        for x in self.events:
            for y in self.events:
                if x != y:
                    if x.isInitialized() and y.isInitialized():
                        if x.timeslot == y.timeslot and x.room == y.room:
                            return False
                    else:
                        return False
        return True

