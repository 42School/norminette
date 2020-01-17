errors = {
    1000: "function has too many arguments.",
    1001: "function missing 'void' qualifier.",
    1002: "missing paramater name or type qualifier.",
    ### This is a dummy rule
    9999: "Consecutive newlines."
}


class NormError:
    def __init__(self, errno, line, col=None):
        self.errno = errno
        self.line = line
        self.col = col
        self.msg = f"{errors.get(self.errno, 'ERROR NOT FOUND')}"

    def __str__(self):
        return f"E{self.errno}({self.line}, {self.col}):\t " + self.msg
