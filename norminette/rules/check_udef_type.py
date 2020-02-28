from lexer import Token
from rules import PrimaryRule


class CheckUdefType(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 10

    def run(self, context):
        return False, 0
