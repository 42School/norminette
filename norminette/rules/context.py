class Context:
    def __init__(self, filename):
        self.filetype = filename.split('.')[-1]
        self.indent_lvl = 0
        self.scope = "global"
        self.line = 0
        self.errors = []
