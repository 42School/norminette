errors = {
    1000: "function declared line {self.line} has too many arguments.",
    1001: "function declared line {self.line} missing 'void' qualifier.",
    1002: "missing paramater name or type qualifier line {self.line}."
}


class NormError:
    def __init__(self, errno, line, col=None):
        self.errno = errno
        self.line = line
        self.col = col

    def __str__(self):
        return f"Error (E{self.errno}): {errors.get(self.errno)}"
