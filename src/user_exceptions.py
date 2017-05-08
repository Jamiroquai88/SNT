class TIMParserException(RuntimeError):
    def __init__(self, arg):
        self.args = [arg]


class EventsException(RuntimeError):
    def __init__(self, arg):
        self.args = [arg]


class TimeTableException(RuntimeError):
    def __init__(self, arg):
        self.args = [arg]


class PopulationException(RuntimeError):
    def __init__(self, arg):
        self.args = [arg]
