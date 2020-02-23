from norm_error import NormError


class Context:
    def __init__(self, filename, tokens):
        self.filename = filename
        self.filetype = filename.split('.')[-1]
        self.tokens = tokens
        self.history = []
        self.errors = []
        self.tkn_scope = len(tokens)
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

    def pop_tokens(self, stop):
        self.tokens = self.tokens[stop:]

    def check_token(self, pos, value):
        tkn = self.peek_token(pos)
        if tkn is None:
            return False
        if isinstance(value, list):
            if tkn.type in value:
                return True
            else:
                return False
        else:
            if tkn.type == value:
                return True
            else:
                return False

    def new_error(self, errno, tkn):
        self.errors.append(NormError(errno, tkn.pos[0], tkn.pos[1]))

    def get_parent_rule(self):
        if len(self.history) == 0:
            return ""
        return self.history[-1 if len(self.history) == 1 else -2]
