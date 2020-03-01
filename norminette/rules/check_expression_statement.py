from rules import PrimaryRule


class CheckExpressionStatement(PrimaryRule):
    def run(self, context):
        return False, 0
    pass
