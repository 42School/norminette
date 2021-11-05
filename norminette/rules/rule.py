class Rule:
    def __init__(self):
        self.name = type(self).__name__
        self.depends_on = []
        self.primary = False

    def register(self, registry):
        if self.depends_on == []:
            if "all" in registry.dependencies:
                registry.dependencies["all"].append(self.name)
            else:
                registry.dependencies["all"] = [self.name]

        for rule in self.depends_on:
            if rule in registry.dependencies:
                registry.dependencies[rule].append(self.name)
            else:
                registry.dependencies[rule] = [self.name]

class PrimaryRule(Rule):
    def __init__(self):
        super().__init__()
        self.primary = True
        self.priority = 0
        self.scope = []

    def run(self, context):
        return False, 0
