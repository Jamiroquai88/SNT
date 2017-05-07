#! /usr/bin/env python

import copy
import random
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from src.event import Event
from src.parser import TIMParser
from src.timetable import TimeTable

if __name__ == "__main__":
    tim_parser = TIMParser()
    events, rooms, features, students = tim_parser.parseInput('datasets/competition/competition06.tim')

    t = TimeTable(events, rooms, features, students)

    end_iter = False

    while True:
        print 'Running from scratch ...'
        events.initTimeslots(t.timeslots, rooms.roomsNumber)

        for i in range(t.timeslots):
            G = nx.Graph()
            G.add_nodes_from(events.getByTimeslot(i), bipartite=0)
            G.add_nodes_from(rooms.rooms, bipartite=1)
            for e in events.getByTimeslot(i):
                for r in rooms:
                    if set(e.features).issubset(r.features):
                        G.add_edge(e, r)
            bmm = nx.bipartite.maximum_matching(G)
            for x in bmm.keys():
                if isinstance(x, Event):
                    x.room = bmm[x]
            del G
        if t.isFeasible():
            break

        iter_count = 0
        while True:
            # M1
            if iter_count == 200:
                break
            feasible_events = t.getFeasibles()
            random_event = events.get(np.random.randint(0, events.eventsNumber))
            if random_event in feasible_events:
                continue
            else:
                if random.uniform(0, 1) > 0.5:
                    if not t.findFeasible(random_event):
                        continue
                else:
                    random_event.timeslot = None
                    random_event.room = None
            # while True:
            #     e1 = events.get(np.random.randint(0, events.eventsNumber))
            #     e2 = events.get(np.random.randint(0, events.eventsNumber))
            #     if e1 in feasible_events or e2 in feasible_events:
            #         continue
            #     e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
            #     e1.room, e2.room = e2.room, e1.room
            #     if t.isFeasible(e1) and t.isFeasible(e2):
            #         break
            #     else:
            #         e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
            #         e1.room, e2.room = e2.room, e1.room
            if len(t.getFeasibles()) == events.eventsNumber:
                end_iter = True
            if len(feasible_events) <= len(t.getFeasibles()):
                iter_count += 1
        if end_iter:
            break
        else:
            print 'Number of feasible events:', len(feasible_events)
