from rules import Rule


class CheckNestOperators(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        return False, 0
