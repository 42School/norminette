errors = {
    1000: "space/tabs before function type.",
    1001: "function missing 'void' qualifier.",
    1002: "missing paramater name or type qualifier.",
    # This is a dummy rule
    9999: "Consecutive newlines."
}


class NormError:
    def __init__(self, errno, line, col=None):
        self.errno = errno
        self.line = line
        self.col = col
        if col is not None:
            self.msg_prefix = f"(line: {self.line}, col: {self.col}):\t"
        else:
            self.msg_prefix = f"(line: {self.line}):\t "
        self.msg = f"{errors.get(self.errno, 'ERROR NOT FOUND')}"

    def __str__(self):
        return f"E{self.errno}" + self.msg_prefix + self.msg
