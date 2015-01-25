import datetime

class DataType(list):
    """Used to represent an abstract type of data that might be given in
    syllabus information. For example, one might have a Date, which must
    be parsed as a valid datetime.Date using one of a number of formats,
    or a day of the week. There may also be a maximum number of fields,
    so a start time might have at most one argument, and meeting days
    might be 7 at most, but exam dates might be arbitrarily many. To
    allow arbitrarily many fields, use 0"""

    class ConstructorNonFunction(Exception): pass
    class InvalidNArgs(Exception): pass
    class TooMuchData(Exception): pass
    class ConstructorException(Exception): pass

    def __init__(self, construct, nargs = 1):
        if construct == None:
            construct = lambda x: x
        elif not callable(construct):
            raise self.ConstructorNonFunction("'%s' is not a function" %
                    construct)

        if type(nargs) != int:
            raise self.InvalidNArgs("NArgs must be an int")

        self.construct = construct
        self.nargs = nargs

    def enter_data(self, string):
        if self.nargs and len(self) >= self.nargs:
            raise self.TooMuchData()

        try:
            self.append(self.construct(string))
        except Exception as e:
            raise self.ConstructorException(e)

    def __str__(self):
        if self.nargs == 1:
            if len(self) > 0:
                return str(self[0])
            else:
                return ""

        return "[ " + ', '.join([str(d) for d in self]) + " ]"

class Time(DataType):
    def __init__(self, nargs = 1):
        super().__init__(self._constructor, nargs)

    @staticmethod
    def _constructor(string):
        return datetime.datetime.strptime(string, "%I:%M %p").time()

class Date(DataType):
    def __init__(self, nargs = 1):
        super().__init__(self._constructor, nargs)

    @staticmethod
    def _constructor(string):
        return datetime.datetime.strptime(string, "%Y-%m-%d").date()

class Weekday(DataType):

    class UnknownWeekday(Exception): pass
    def __init__(self, nargs = 1):
        super().__init__(self._constructor, nargs)

    @staticmethod
    def _constructor(string):
        return string

class Email(DataType):
    def __init__(self, nargs = 1):
        super().__init__(self._constructor, nargs)

    @staticmethod
    def _constructor(string):
        return string.replace(' ', '')

class CourseID(DataType):
    def __init__(self, nargs = 1):
        super().__init__(self._constructor, nargs)

    @staticmethod
    def _constructor(string):
        return string.replace(' ', '')
