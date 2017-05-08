import os
import sys
import copy
import random
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from src.user_exceptions import EventsException


class Events(object):
    def __init__(self, num):
        self.eventsNumber = num
        self.events = []
        self.localSearchIters = 1000

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
        # G = nx.Graph()
        # G.add_nodes_from(self.events)
        # for x, y in itertools.combinations(G.nodes(), 2):
        #     nconflicts = len(set(x.students).intersection(y.students))
        #     if nconflicts > 0:
        #         G.add_edge(x, y, weight=nconflicts)
        # greedy_coloring = nx.coloring.greedy_color(
        #     G, strategy=nx.coloring.strategy_random_sequential)
        # for key, value in greedy_coloring.items():
        #     key.timeslot = value
        # return True
        # cluster_max = max(greedy_coloring.values())
        # if cluster_max >= ntimeslots:
        #     print 'Warning: Too many timeslots!'
        #     return False
        #
        # rdict = {}
        # for e, t in greedy_coloring.items():
        #     if t not in rdict.keys():
        #         rdict[t] = []
        #     rdict[t].append(e)
        #
        # sorted_cluster = []
        # for key in rdict.keys():
        #     sorted_cluster.append((key, len(rdict[key])))
        # sorted_cluster = sorted(sorted_cluster, key=lambda xx: xx[1], reverse=True)
        # if sorted_cluster[0][1] > 2 * nrooms:
        #     return False
        # start_idx = ntimeslots - 1 - cluster_max
        # keep_clusters = []
        # split_clusters = {}
        # for i in range(len(sorted_cluster)):
        #     if i > start_idx:
        #         keep_clusters.append(sorted_cluster[i][0])
        #     else:
        #         split_clusters[sorted_cluster[i][0]] = sorted_cluster[i][1]
        # if sorted_cluster[start_idx][1] > nrooms:
        #     return False
        # else:
        #     for e, t in greedy_coloring.items():
        #         if t in keep_clusters:
        #             e.timeslot = t
        #         else:
        #             cluster_size = len(self.getByTimeslot(t))
        #             # print 'Cluster size:', cluster_size
        #             if cluster_size < split_clusters[t] / 2:
        #                 e.timeslot = t
        #             else:
        #                 e.timeslot = t + cluster_max + 1
        #     return True

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

    # def tabuSearch(self, t, tabu_list):
    #     ts_iter = 0
    #     while True:
    #         if ts_iter > self.tabuSearchIters:
    #             break
    #         print 'Number of feasible events:', len(t.getFeasibles())
    #         unfesiable_events = t.getUnfeasibles()
    #         tl = int(np.random.randint(0, 11) + 0.6 * len(unfesiable_events))
    #         for x in tabu_list[:-tl]:
    #             if not t.findFeasible(x):
    #                 ts_iter += 1

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
