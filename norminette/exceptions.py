class CParsingError(Exception):
    def __init__(self, errmsg):
        self.msg = errmsg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__
