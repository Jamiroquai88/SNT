import copy
import numpy as np

from src.timetable import TimeTable


class Solution(TimeTable):
    def __init__(self, events, rooms, features, students):
        super(TimeTable, self).__init__()
        self.events = copy.deepcopy(events)
        self.rooms = copy.deepcopy(rooms)
        self.features = copy.deepcopy(features)
        self.students = copy.deepcopy(students)
        self.timeslots = 45
        self.dailySlots = 9
        self.days = self.timeslots / self.dailySlots
        self.findFeasibleIters = 1000
        self.randIterImprovementIters = 100


