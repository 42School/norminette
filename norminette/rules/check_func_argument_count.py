class CheckFuncArgumentCount:
    def __init__(self):
        self.name = "CheckFuncArgumentCount"
        self.subrules = []
        pass

    def run(self, context):
        return False, 0
