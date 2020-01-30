from rules import Rule


ps_operators = [ # operators that should be prefixed and suffixed by a space
    "RIGHT_ASSIGN", # >>=
    "LEFT_ASSIGN", # <<=
    "ADD_ASSIGN", # +=
    "SUB_ASSIGN", # -=
    "MUL_ASSIGN", # *=
    "DIV_ASSIGN", # /=
    "MOD_ASSIGN", # %=
    "AND_ASSIGN", # &=
    "XOR_ASSIGN", # ^=
    "OR_ASSIGN", # |=
    "LESS_OR_EQUAL", # <=
    "GREATER_OR_EQUAL", # >=
    "EQUALS", # ==
    "NOT_EQUAL", # !=
    "ASSIGN", # =
    "COLON", # :
    "DIV", # /
    "MODULO", # %
    "LESS_THAN", # <
    "MORE_THAN", # >
    "AND", # &
    "OR", # |
    "BWISE_XOR", # ^
    "BWISE_OR", # |
    "BWISE_NOT", # !
    "BWISE_AND", # &
    "RIGHT_SHIFT", # >>
    "LEFT_SHIFT", # <<
    "TERN_CONDITION" # ?
]

p_operators = [
# operators that should only be prefixed by a space
    "ELLIPSIS" #`...`
]

s_operators = [
# operators that should only be suffixed by a space
    "COMMA" # `,`
]

c_operators = [
# operators that could be "glued" with another token ("x + *y", "5 + -5" ...)
    "PLUS",
    "MINUS",
    "MULT"
]

left_auth = [
]

right_auth = [
]

whitespaces = [
    "NEWLINE",
    "SPACE",
    "TAB"
]


class CheckOperatorsSpacing(Rule):
    def __init__(self):
        super().__init__()
        self.last_seen_tkn = None

    def check_prefix(self, context, pos):
        if pos > 0 and context.peek_token(pos - 1).type != "SPACE":
            context.new_error(1003, context.peek_token(pos - 1))
        if pos + 1 < len(context.tokens[:context.tkn_scope]) \
                and context.peek_token(pos + 1).type == "SPACE":
            context.new_error(1006, context.peek_token(pos + 1))

    def check_suffix(self, context, pos):
        if pos + 1 < len(context.tokens[:context.tkn_scope]) \
                and context.peek_token(pos + 1).type != "SPACE":
            context.new_error(1004, context.peek_token(pos + 1))
        if pos > 0 and context.peek_token(pos - 1).type == "SPACE":
            context.new_error(1005, context.peek_token(pos - 1))

    def check_combined_op(self):
        if self.last_seen_tkn.type in []:
            pass
        pass

    def check_prefix_and_suffix(self, context, pos):
        if pos > 0 and context.peek_token(pos - 1).type != "SPACE":
            context.new_error(1003, context.peek_token(pos - 1))
        if pos + 1 < len(context.tokens[:context.tkn_scope]) \
                and context.peek_token(pos + 1).type != "SPACE":
            context.new_error(1004, context.peek_token(pos + 1))

    def run(self, context):
        self.last_seen_tkn = None
        i = 0
        while i < len(context.tokens[:context.tkn_scope]):
            if context.peek_token(i).type not in whitespaces:
                self.last_seen_tkn = context.peek_token(i)
            if context.peek_token(i).type in ps_operators:
                self.check_prefix_and_suffix(context, i)
            elif context.peek_token(i).type in s_operators:
                self.check_suffix(context, i)
            elif context.peek_token(i).type in p_operators:
                self.check_prefix(context, i)
            i += 1
        return True, 0
