#! /usr/bin/env python

import argparse
import sys
import os

from src.parser import TIMParser
from src.population import Population


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='University course timetabling problem.')
    parser.add_argument('-i', action='store', dest='input_file', type=str, required=True)
    r = parser.parse_args()

    tim_parser = TIMParser()
    events, rooms, features, students = tim_parser.parseInput(r.input_file)

    population = Population(events, rooms, features, students)

