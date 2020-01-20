from rules.norm_error import NormError


class Context:
    def __init__(self, filename, tokens, rules):
        self.filename = filename
        self.filetype = filename.split('.')[-1]
        self.tokens = tokens
        self.rules = rules
        self.errors = []
        self.scope = "global"
        self.indent_lvl = 0
        self.lines = 1
        self.functions = 0
        self.declarations_allowed = True

    def peekToken(self, pos):
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def popTokens(self, stop):
        for i in range(stop):
            if self.peekToken(i) is not None \
                    and self.peekToken(i).type == "NEWLINE":
                self.lines += 1
        self.tokens = self.tokens[stop:]

    def pushError(self, errno, tkn):
        self.errors.append(NormError(errno, tkn.pos[0], tkn.pos[1]))
