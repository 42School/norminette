from rules import Rule


class CheckFuncArgumentCount(Rule):
    def run(self, context):
        return False, 0
