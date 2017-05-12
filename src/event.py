import copy
import itertools
import numpy as np
import networkx as nx


class Events(object):
    def __init__(self, num):
        self.eventsNumber = num
        self.events = []
        self.localSearchIters = 10

    def __iter__(self):
        current = 0
        while current < len(self.events):
            yield self.events[current]
            current += 1

    def addEvent(self):
        self.events.append(Event(len(self.events)))

    def get(self, idx):
        return self.events[idx]

    def getLast(self):
        return self.events[-1]

    def getByTimeslot(self, timeslot):
        a = []
        for x in self.events:
            if x.timeslot == timeslot:
                a.append(x)
        return a

    def getStudentsBySlot(self, timeslot):
        a = self.getByTimeslot(timeslot)
        b = set()
        for x in a:
            for s in x.students:
                b.add(s)
        return list(b)

    def initTimeslots(self, ntimeslots):
        events_copy = copy.copy(self.events)
        for i in range(self.eventsNumber):
            G = nx.Graph()
            G.add_nodes_from(events_copy)
            for x, y in itertools.combinations(G.nodes(), 2):
                nconflicts = len(set(x.students).intersection(y.students))
                if nconflicts > 0:
                    G.add_edge(x, y, weight=nconflicts)
            greedy_coloring = nx.coloring.greedy_color(G, strategy=nx.coloring.strategy_largest_first)
            max_degree = max(greedy_coloring.values())
            for x in greedy_coloring:
                if greedy_coloring[x] == max_degree:
                    x.timeslot = np.random.randint(0, ntimeslots)
                    events_copy.remove(x)
                    del G
                    break
        return True

    def initRooms(self, ntimeslots, rooms):
        for i in range(ntimeslots):
            G = nx.Graph()
            G.add_nodes_from(self.getByTimeslot(i), bipartite=0)
            G.add_nodes_from(rooms.rooms, bipartite=1)
            for e in self.getByTimeslot(i):
                for r in rooms:
                    if set(e.features).issubset(r.features):
                        G.add_edge(e, r)
            bmm = nx.bipartite.maximum_matching(G)
            for x in bmm.keys():
                if isinstance(x, Event):
                    x.room = bmm[x]
            del G
        return True

    def localSearch(self, t):
        iter_count = 0
        while True:
            if iter_count == self.localSearchIters:
                return False
            feasible_len = len(t.getFeasibles())
            random_event = self.get(np.random.randint(0, self.eventsNumber))
            if not t.findFeasible(random_event):
                continue
            while True:
                e1 = self.get(np.random.randint(0, self.eventsNumber))
                e2 = self.get(np.random.randint(0, self.eventsNumber))
                e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
                e1.room, e2.room = e2.room, e1.room
                if t.isFeasible(e1) and t.isFeasible(e2):
                    break
                else:
                    e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
                    e1.room, e2.room = e2.room, e1.room
            feas_len = len(t.getFeasibles())

            if feas_len == self.eventsNumber:
                return True
            if feasible_len >= feas_len:
                iter_count += 1
            else:
                iter_count = 0
            print 'Number of feasible events:', feas_len, 'counter:', iter_count

    def mutation(self, event):
        pass


class Event(object):
    def __init__(self, idx):
        self.index = idx
        self.students = []
        self.features = []
        self.room = None
        self.timeslot = None

    def addStudent(self, student):
        self.students.append(student)

    def addFeature(self, feature):
        self.features.append(feature)

    def isInitialized(self):
        return self.room is not None and self.timeslot is not None
