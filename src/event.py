import os
import sys
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

    def initTimeslots(self, ntimeslots, nrooms):
        G = nx.Graph()
        G.add_nodes_from(self.events)
        for x, y in itertools.combinations(G.nodes(), 2):
            nconflicts = len(set(x.students).intersection(y.students))
            if nconflicts > 0:
                G.add_edge(x, y, weight=nconflicts)
        greedy_coloring = nx.coloring.greedy_color(
            G, strategy=nx.coloring.strategy_random_sequential)
        for key, value in greedy_coloring.items():
            key.timeslot = value
        return True
        cluster_max = max(greedy_coloring.values())
        if cluster_max >= ntimeslots:
            print 'Warning: Too many timeslots!'
            return False

        rdict = {}
        for e, t in greedy_coloring.items():
            if t not in rdict.keys():
                rdict[t] = []
            rdict[t].append(e)

        sorted_cluster = []
        for key in rdict.keys():
            sorted_cluster.append((key, len(rdict[key])))
        sorted_cluster = sorted(sorted_cluster, key=lambda xx: xx[1], reverse=True)
        if sorted_cluster[0][1] > 2 * nrooms:
            return False
        start_idx = ntimeslots - 1 - cluster_max
        keep_clusters = []
        split_clusters = {}
        for i in range(len(sorted_cluster)):
            if i > start_idx:
                keep_clusters.append(sorted_cluster[i][0])
            else:
                split_clusters[sorted_cluster[i][0]] = sorted_cluster[i][1]
        if sorted_cluster[start_idx][1] > nrooms:
            return False
        else:
            for e, t in greedy_coloring.items():
                if t in keep_clusters:
                    e.timeslot = t
                else:
                    cluster_size = len(self.getByTimeslot(t))
                    # print 'Cluster size:', cluster_size
                    if cluster_size < split_clusters[t] / 2:
                        e.timeslot = t
                    else:
                        e.timeslot = t + cluster_max + 1
            return True

    def initRooms(self, ntimeslots, rooms):
        print 'init rooms'
        # G = nx.Graph()
        # G.add_nodes_from(self.events)
        for i in range(ntimeslots):
            events = self.getByTimeslot(i)
            for x in events:
                x.room = None
            print 'Timeslot:', i, len(events)
            # counter = 0
            for x in itertools.permutations(range(len(events)), len(events)):
                # counter += 1
                # print counter
                for y in x:
                    # print y
                    e = events[y]
                    r = rooms.get(y)
                    if set(e.features).issubset(r.features) and len(e.students) <= r.size:
                        print 'Setting room:', events.index(e)
                        e.room = r
                    else:
                        break
            for x in events:
                if x.room is None:
                    print 'Room not initialized!', events.index(x)
                    return False
            print 'DONE', i
        return True


        rooms_len = len(rooms)
        for x in self.events:
            for r in random.sample(rooms, rooms_len):
                rfound = False
                for y in self.getByTimeslot(x.timeslot):
                    if x != y:
                        if x.room == y.room:
                            rfound = True
                if rfound:
                    continue
                else:
                    if set(x.features).issubset(r.features) and len(x.students) <= r.size:
                        x.room = r
            if x.room is None:
                print 'could not satisfy room'
                return False
        print 'rooms satisfied'
        return True


        # G2 = nx.Graph()
        # G2.add_nodes_from(random.sample(self.events, self.eventsNumber))
        # for x, y in itertools.combinations(G2.nodes(), 2):
        #     if x.timeslot == y.timeslot:
        #         G2.add_edge(x, y, weight=1)
        # greedy_coloring = nx.coloring.greedy_color(
        #     G2, strategy=nx.coloring.strategy_random_sequential, interchange=True)
        # print greedy_coloring
        # print max(greedy_coloring.values())
        # for key, room in greedy_coloring.items():
        #     if room < rooms_len:
        #         key.room = room
        #     else:
        #         return False
        # return True
        # nx.draw(G2)
        # plt.show()
        # for e in self.events:
        #     if e.room is None:
        #         for r in random.sample(rooms, len(rooms)):
        #             if set(e.features).issubset(r.features) and len(e.students) <= r.size:
        #                 e.room = r
        #                 break
        #         if e.room is None:
        #             print 'impossible to satisfy features'
        #             return False
        # for x, y in itertools.combinations(self.events, 2):
        #     if x.timeslot == y.timeslot and x.room == y.room:
        #         x.room, y.room = None, None
        #         return False
        #         cnt += 1
        #         G2.add_edge(x.room, y.room)
        # print nx.coloring.greedy_color(G2, strategy=nx.coloring.strategy_largest_first).values()
        # nx.draw(G2)
        # plt.show()
        # for key, room in nx.coloring.greedy_color(G2, strategy=nx.coloring.strategy_largest_first).items():
        #     print 'assigning room'
        #     key.room = rooms[room % len(rooms) - 1]
        # G = nx.Graph()
        # G.add_nodes_from(rooms)
        # print rooms
        # for x, y in itertools.combinations(G.nodes(), 2):
        #     if x.room == y.room:
        #         print 'adding edge'
        #         G.add_edge(rooms[rooms.index(x.room)], rooms[rooms.index(y.room)], weight=1)
        # print nx.coloring.greedy_color(G, strategy=nx.coloring.strategy_largest_first)
        # nx.draw(G)
        # plt.show()


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
