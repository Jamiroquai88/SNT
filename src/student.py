
class Students(object):
    def __init__(self, num):
        self.current = 0
        self.studentsNumber = num
        self.students = []

    def __iter__(self):
        current = 0
        while current < len(self.students):
            yield self.students[current]
            current += 1

    def addStudent(self):
        self.students.append(Student(len(self.students)))

    def getLast(self):
        return self.students[-1]


class Student(object):
    def __init__(self, idx):
        self.index = idx
