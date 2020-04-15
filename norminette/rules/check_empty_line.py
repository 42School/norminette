from rules import Rule
from scope import *



class CheckEmptyLine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        #allowed
        # -> newline in between functions or declarations
        # -> newline in function between declaration and the rest

        #not allowed
        # -> consecutive newlines
        # -> newline at the end of file

        return False, 0
