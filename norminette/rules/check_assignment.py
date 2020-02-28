from rules import Rule


class CheckAssignment(Rule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 5

    def run(self, context):
        return False, 0
