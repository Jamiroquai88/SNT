#! /usr/bin/env python

import copy
import random
import argparse
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from src.event import Event
from src.parser import TIMParser
from src.timetable import TimeTable

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='University course timetabling problem.')
    parser.add_argument('-i', action='store', dest='input_file', type=str, required=True)
    r = parser.parse_args()

    tim_parser = TIMParser()
    events, rooms, features, students = tim_parser.parseInput(r.input_file)
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
            if iter_count == 100:
                break
            feasible_events = t.getFeasibles()
            unfesiable_events = t.getUnfeasibles()
            random_event = unfesiable_events[np.random.randint(0, len(unfesiable_events))]
            if random.uniform(0, 1) > 0.5:
                if not t.findFeasible(random_event):
                    continue
            else:
                random_event.timeslot = None
                random_event.room = None
            inner_iter_count = 0
            while True:
                unfesiable_events = t.getUnfeasibles()
                e1 = unfesiable_events[np.random.randint(0, len(unfesiable_events))]
                e2 = unfesiable_events[np.random.randint(0, len(unfesiable_events))]
                e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
                e1.room, e2.room = e2.room, e1.room
                if t.isFeasible(e1) or t.isFeasible(e2):
                    break
                else:
                    e1.timeslot, e2.timeslot = e2.timeslot, e1.timeslot
                    e1.room, e2.room = e2.room, e1.room
                    inner_iter_count += 1
                    if inner_iter_count == 10:
                        break
            feas_len = len(t.getFeasibles())
            print 'Number of feasible events:', feas_len, 'counter:', iter_count
            if feas_len == events.eventsNumber:
                end_iter = True
            if len(feasible_events) >= feas_len:
                iter_count += 1
            else:
                iter_count = 0
        if end_iter:
            break
        else:
            print 'Number of feasible events:', len(feasible_events)

        # tabu search
        ts_iter = 0
        while True:
            if ts_iter > 100:
                break
            unfesiable_events = t.getUnfeasibles()
            tl = int(np.random.randint(0, 11) + 0.6 * len(unfesiable_events))
            if tl < len(unfesiable_events):
                random_event = unfesiable_events[tl]
                if not t.findFeasible(random_event):
                    ts_iter += 1

