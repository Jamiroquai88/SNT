#! /usr/bin/env python

import sys
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
        events_copy = copy.copy(events.events)




        if t.isFeasible():
            break



        # tabu search





