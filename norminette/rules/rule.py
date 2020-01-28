class Rule:
    def __init__(self):
        self.name = type(self).__name__
        self.dependencies = []
        self.primary = False
