from rules import Rule


class CheckPreprocessorDefine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [""]
