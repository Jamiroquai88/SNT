from event import Events
from room import Rooms
from feature import Features
from student import Students

from user_exceptions import TIMParserException


class TIMParser(object):
    def __init__(self):
        self.inputFile = None
        self.outputFile = None

    def parseInput(self, f):
        self.inputFile = f
        with open(f) as file:
            lines = file.readlines()
        first_line = lines[0].split()
        print first_line
        events = Events(int(first_line[0]))
        rooms = Rooms(int(first_line[1]))
        features = Features(int(first_line[2]))
        students = Students(int(first_line[3]))
        print 'Lengths:', events.eventsNumber, rooms.roomsNumber, features.featuresNumber, students.studentsNumber
        for size in lines[1:rooms.roomsNumber + 1]:
            print 'Size:', size
            rooms.addRoom(int(size))
        offset = rooms.roomsNumber + 1
        for ii in range(students.studentsNumber):
            students.addStudent()
            for jj in range(events.eventsNumber):
                if ii == 0:
                    events.addEvent()
                e = events.get(jj)
                attends = int(lines[ii * events.eventsNumber + jj + offset])
                print 'Event:', jj, ', student:', ii, '-', attends
                if attends == 1:
                    e.addStudent(students.getLast())
                elif attends == 0:
                    pass
                else:
                    raise TIMParserException(
                        '[parseInput] Unexpected value when adding student to event!'
                    )
        offset += events.eventsNumber * students.studentsNumber
        for ii in range(rooms.roomsNumber):
            r = rooms.get(ii)
            for jj in range(features.featuresNumber):
                if ii == 0:
                    features.addFeature()
                fea = int(lines[ii * features.featuresNumber + jj + offset])
                if fea == 1:
                    r.addFeature(features.get(jj))
                elif fea == 0:
                    pass
                else:
                    raise TIMParserException(
                        '[parseInput] Unexpected value when adding feature to room!'
                    )
        offset += rooms.roomsNumber * features.featuresNumber
        for ii in range(events.eventsNumber):
            e = events.get(ii)
            for jj in range(features.featuresNumber):
                fea = int(lines[ii * features.featuresNumber + jj + offset])
                if fea == 1:
                    e.addFeature(features.get(jj))
                elif fea == 0:
                    pass
                else:
                    raise TIMParserException(
                        '[parseInput] Unexpected value when adding feature to event!'
                    )
        print offset + events.eventsNumber * features.featuresNumber, len(lines)
        if offset + events.eventsNumber * features.featuresNumber != len(lines):
            raise TIMParserException(
                '[parseInput] Unexpected number of lines in input file!'
            )
        return events, rooms, features, students
