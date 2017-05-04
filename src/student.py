
class Students(object):
    def __init__(self, num):
        self.current = 0
        self.studentsNumber = num
        self.students = []

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.students):
            raise StopIteration
        else:
            self.current += 1
            return self.students[self.current - 1]

    def addStudent(self):
        self.students.append(Student(len(self.students)))

    def getLast(self):
        return self.students[-1]


class Student(object):
    def __init__(self, idx):
        self.index = idx
