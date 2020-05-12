from rules import Rule

operators = [
    "RIGHT_ASSIGN",
    "LEFT_ASSIGN",
    "ADD_ASSIGN",
    "SUB_ASSIGN",
    "MUL_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "XOR_ASSIGN",
    "OR_ASSIGN",
    "LESS_OR_EQUAL",
    "GREATER_OR_EQUAL",
    "EQUALS",
    "NOT_EQUAL",
    "ASSIGN",
    # "COLON",
    # "SEMI_COLON",
    # "COMMA",
    # "DOT",
    "NOT",
    "MINUS",
    "PLUS",
    "MULT",
    "DIV",
    "MODULO",
    "LESS_THAN",
    "MORE_THAN",
    "ELLIPSIS",
    "INC",
    "DEC",
    "PTR",
    "AND",
    "OR",
    "BWISE_XOR",
    "BWISE_OR",
    "BWISE_NOT",
    "BWISE_AND",
    "RIGHT_SHIFT",
    "LEFT_SHIFT",
    "TERN_CONDITION"
]

assign_operators = [
    "RIGHT_ASSIGN",
    "LEFT_ASSIGN",
    "ADD_ASSIGN",
    "SUB_ASSIGN",
    "MUL_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "XOR_ASSIGN",
    "OR_ASSIGN",
    "ASSIGN"
]

ps_operators = [
    # operators that should be prefixed and suffixed by a space
    "RIGHT_ASSIGN",  # >>=
    "LEFT_ASSIGN",  # <<=
    "ADD_ASSIGN",  # +=
    "SUB_ASSIGN",  # -=
    "MUL_ASSIGN",  # *=
    "DIV_ASSIGN",  # /=
    "MOD_ASSIGN",  # %=
    "AND_ASSIGN",  # &=
    "XOR_ASSIGN",  # ^=
    "OR_ASSIGN",  # |=
    "LESS_OR_EQUAL",  # <=
    "GREATER_OR_EQUAL",  # >=
    "EQUALS",  # ==
    "NOT_EQUAL",  # !=
    "ASSIGN",  # =
    "COLON",  # :
    "DIV",  # /
    "MODULO",  # %
    "LESS_THAN",  # <
    "MORE_THAN",  # >
    "AND",  # &
    "OR",  # |
    "BWISE_XOR",  # ^
    "BWISE_OR",  # |
    "BWISE_NOT",  # !
    "BWISE_AND",  # &
    "RIGHT_SHIFT",  # >>
    "LEFT_SHIFT",  # <<
    "TERN_CONDITION"  # ?
]

p_operators = [
    # operators that should only be prefixed by a space
    "ELLIPSIS"  # ...
]

s_operators = [
    # operators that should only be suffixed by a space
    "COMMA"  # ,
]

son_operators = [
    # operators that should only be suffixed by a space or newline
    "SEMI_COLON"  # ;
]

c_operators = [
    # operators that could be "glued" with another token ("x + *y", "5 + -5")
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
        self.depends_on = [
            "IsFuncDeclaration",
            "IsFuncPrototype",
            "IsExpressionStatement",
            "IsAssignation",
            "IsControlStatement",
            "IsUserDefinedType"
        ]
        self.last_seen_tkn = None

    def check_prefix(self, context, pos):
        tmp = -1

        if pos > 0 and context.peek_token(pos - 1).type != "SPACE":
            context.new_error("SPC_BFR_OPERATOR", context.peek_token(pos))
        if pos + 1 < len(context.tokens[:context.tkn_scope]) \
                and context.peek_token(pos + 1).type == "SPACE":
            context.new_error("NO_SPC_AFR_OPR", context.peek_token(pos))

    def check_suffix(self, context, pos):
        if pos + 1 < len(context.tokens[:context.tkn_scope]) \
                and not context.check_token(pos + 1, ["SPACE", "NEWLINE"]):
            context.new_error("SPC_AFTER_OPERATOR", context.peek_token(pos))
        if pos > 0 and context.peek_token(pos - 1).type == "SPACE":
            context.new_error("NO_SPC_BFR_OPR", context.peek_token(pos))

    def check_prefix_and_suffix(self, context, pos):
        if pos > 0 and context.peek_token(pos - 1).type != "SPACE":
            if context.check_token(pos - 1, "TAB") is True:
                tmp = -1
                while context.check_token(pos + tmp, "TAB") is True:
                    tmp -= 1
                if context.check_token(pos + tmp, "NEWLINE") is True:
                    return False, 0
            context.new_error("SPC_BFR_OPERATOR", context.peek_token(pos))
        if pos + 1 < len(context.tokens[:context.tkn_scope]) \
                and context.peek_token(pos + 1).type != "SPACE":
            context.new_error("SPC_AFTER_OPERATOR", context.peek_token(pos))

    def check_combined_op(self, context, pos):
        lpointer = ["SPACE", "TAB", "LPARENTHESIS", "LBRACKET"]
        lsign = operators + ["LBRACKET"]
        i = 0
        if context.peek_token(pos).type in ["PLUS", "MINUS"]:
            if self.last_seen_tkn.type in lsign:
                if pos > 0 and context.peek_token(pos - 1).type != "SPACE":
                    context.new_error("SPC_BFR_OPERATOR", context.peek_token(pos))
                i = 1
                while context.peek_token(pos + i).type \
                        in ["PLUS", "MINUS", "MULT"]:
                    i += 1
                if context.peek_token(pos + i).type in ["SPACE", "TAB"]:
                    context.new_error("NO_SPC_AFR_OPR", context.peek_token(pos + i - 1))
                return i
            else:
                self.check_prefix_and_suffix(context, pos)
                return 1
        if context.peek_token(pos).type == "MULT":
            has_initial_id = False
            tmp = 0
            while context.check_token(tmp, ["IDENTIFIER", "SEMI_COLON", "NEWLINE"]) is False:
                tmp += 1
            if context.check_token(tmp, "IDENTIFIER") is True:
                has_initial_id = True
            if context.check_token(pos - 1, lpointer) == False:
                context.new_error("SPC_BFR_POINTER", context.peek_token(pos))
            if context.check_token(pos + 1, ["SPACE", "TAB"]) and has_initial_id == True:
                context.new_error("SPC_AFTER_POINTER", context.peek_token(pos))
            elif context.check_token(pos + 1, ["SPACE", "TAB"]) is False \
                and has_initial_id == False:
                context.new_error("SPC_AFTER_OPERATOR", context.peek_token(pos))
            i = 1
            while context.peek_token(pos + i).type in ["MULT", "LPARENTHESIS"]:
                i += 1
                if context.peek_token(pos + i).type == "SPACE":
                    context.new_error("SPC_AFTER_POINTER", context.peek_token(pos + i))
                return (i)

    def run(self, context):
        self.last_seen_tkn = None
        i = 0
        while i < len(context.tokens[:context.tkn_scope]):
            if context.check_token(i, c_operators):
                pos = i
                val = self.check_combined_op(context, i)
                if val == None:
                    return False, 0
                i += val
                self.last_seen_tkn = context.peek_token(pos)
                continue
            elif context.peek_token(i).type in ps_operators:
                self.check_prefix_and_suffix(context, i)
            elif context.peek_token(i).type in s_operators:
                self.check_suffix(context, i)
            elif context.peek_token(i).type in son_operators and \
                context.check_token(i + 1, "NEWLINE") is False:
                self.check_suffix(context, i)
            elif context.peek_token(i).type in p_operators:
                self.check_prefix(context, i)
            if context.peek_token(i).type not in whitespaces:
                self.last_seen_tkn = context.peek_token(i)
            i += 1
        return True, 0
