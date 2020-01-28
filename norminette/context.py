from norm_error import NormError


class Context:
    def __init__(self, filename, tokens):
        self.filename = filename
        self.filetype = filename.split('.')[-1]
        self.tokens = tokens
        self.errors = []
        self.tkn_scope = 0
        self.indent_lvl = 0
        self.lines = 1
        self.functions_declared = 0
        self.var_declared = 0
        self.global_scope = True
        self.declarations_allowed = True

    def peek_token(self, pos):
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def pop_tokens(self, stop):
        for i in range(stop):
            if self.peek_token(i) is not None \
                    and self.peek_token(i).type == "NEWLINE":
                self.lines += 1
        self.tokens = self.tokens[stop:]

    def new_error(self, errno, tkn):
        self.errors.append(NormError(errno, tkn.pos[0], tkn.pos[1]))
