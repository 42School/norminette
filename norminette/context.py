from norm_error import NormError
from lexer.dictionary import operators, brackets


class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.name = type(self).__name__
        self.lvl = (parent.lvl + 1) if parent is not None else 0
        self.indent = (parent.indent + 1) if parent is not None else 0
        self.lines = 0
        # ########################################################## #
        self.vdeclarations_allowed = True
        self.vars = 0
        self.vars_alignment = 0
        # ########################################################## #
        self.fdeclarations_allowed = False  # False everywhere but GlobalScope

    def inner(self, sub):
        return sub(self)

    def outer(self):
        if self.parent is not None:
            self.parent.lines += self.lines
        return self.parent


class GlobalScope(Scope):
    def __init__(self):
        super().__init__()
        self.fdeclarations_allowed = True
        self.fnames = []
        self.functions = 0
        self.func_alignment = 0
    pass


class Function(Scope):
    pass


class ControlStructure(Scope):
    pass


class UserDefinedType(Scope):
    pass


class VariableAssignation(Scope):
    pass


class Context:
    def __init__(self, filename, tokens):
        # File relative informations
        self.filename = filename
        self.filetype = filename.split('.')[-1]  # ?
        self.tokens = tokens

        # Rule relative informations
        self.history = []
        self.errors = []
        self.tkn_scope = len(tokens)

        # Scope informations
        self.scope = GlobalScope()
        self.fname_pos = 0
        self.arg_pos = [0, 0]

    def dprint(self, rule, pos):
        print(f"{self.filename} - {rule} in {self.scope.name}:")
        i = 0
        for t in self.tokens[:pos]:
            if i == 0:
                print("\t\t", end="")
            if t.type == "NEWLINE":
                print(t)
                i = 0
            else:
                print(t, end=" ")
                i += 1
        print("")

    def peek_token(self, pos):
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def pop_tokens(self, stop):
        self.tokens = self.tokens[stop:]

    def clean(self):
        self.arg_pos = []

    def check_token(self, pos, value):
        tkn = self.peek_token(pos)
        if tkn is None:
            return False
        if isinstance(value, list):
            if tkn.type in value:
                return True
            return False
        else:
            return tkn.type == value

    def new_error(self, errno, tkn):
        self.errors.append(NormError(errno, tkn.pos[0], tkn.pos[1]))

    def get_parent_rule(self):
        if len(self.history) == 0:
            return ""
        return self.history[-1 if len(self.history) == 1 else -2]

    def update(self):
        if self.history[0].scope is not None:
            if self.history[0].scope is self.scope.parent:
                self.scope.outer()
            else:
                self.scope.inner(self.history[0].scope)
        pass
