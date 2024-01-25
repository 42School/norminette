class NorminetteError(Exception):
    pass


class CParsingError(NorminetteError):
    def __init__(self, errmsg):
        self.msg = errmsg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__


class MaybeInfiniteLoop(NorminetteError):
    def __init__(self) -> None:
        super().__init__("The maximum number of iterations a loop can have has been reached")


class UnexpectedEOF(NorminetteError):
    pass
