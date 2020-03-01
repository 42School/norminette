from rules import PrimaryRule


class CheckAssignation(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 5

    def run(self, context):
        i = self.skip_ws(context, 0)
        return False, 0
