from rules import PrimaryRule


class CheckInstruction(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 1

    def run(self, context):
        return False, 0
