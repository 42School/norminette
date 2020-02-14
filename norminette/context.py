from norm_error import NormError


class Context:
    def __init__(self, filename, tokens):
        self.filename = filename
        self.filetype = filename.split('.')[-1]
        self.tokens = tokens
        self.history = []
        self.errors = []
        self.tkn_scope = 0
        self.indent_lvl = 0
        self.lines = 0
        self.functions_declared = 0
        self.var_declared = [0]
        self.var_alignment = [0]
        self.global_scope = True
        self.scope_lvl = 0
        self.declarations_allowed = True

    def peek_token(self, pos):
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def eat_tokens(self, stop):
        self.tokens = self.tokens[stop:]

    def new_error(self, errno, tkn):
        self.errors.append(NormError(errno, tkn.pos[0], tkn.pos[1]))

    def get_parent_rule(self):
        if len(self.history) == 0:
            return ""
        return self.history[-1 if len(self.history) == 1 else -2]
