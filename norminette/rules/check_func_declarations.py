from .norm_error import NormError
from lexer import Token

type_specifiers = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "UNION",
    "VOID",
]

misc_specifiers = [
    "CONST",
    "REGISTER",
    "STATIC",
    "STRUCT",
    "VOLATILE"
]

size_specifiers = [
    "LONG",
    "SHORT"
]

sign_specifiers = [
    "SIGNED",
    "UNSIGNED"
]

whitespaces = [
    "SPACE",
    "TAB",
    "NEWLINE"
]

arg_separator = [
    "OP_COMMA",
    "CLOSING_PARENTHESIS"
]


class CheckFuncDeclarations:
    def __init__(self):
        self.name = "CheckFuncDeclaration"
        self.subrules = ["CheckFuncArgumentCount", "CheckSpacing"]
        self.__i = 0

    def skip_ws(self, context, pos):
        i = pos
        while context.peekToken(i) is not None \
                and context.peekToken(i).type in whitespaces:
            i += 1
        return i

    def check_functype_prefix(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)

        if context.peekToken(i) is not None \
                and context.peekToken(i).type in misc_specifiers:
            # Skipping "const/register/struct/static/volatile" keywords
            i += 1
            i = self.skip_ws(context, i)

        if context.peekToken(i) is not None \
                and context.peekToken(i).type in sign_specifiers:
            # This case is the 'trickier'
            # sign specifier (signed, unsigned) can be followed by:
            # optionnal size specifier (long, short)
            # AND/OR optionnal type specifier (int, char)
            i += 1
            i = self.skip_ws(context, i)
            if context.peekToken(i) is not None \
                    and context.peekToken(i).type in size_specifiers:
                i += 1
                i = self.skip_ws(context, i)
                if context.peekToken(i) is not None \
                        and context.peekToken(i).type in type_specifiers:
                    i += 1
                    i = self.skip_ws(context, i)
                    return True, i
                return True, i

            else:
                return True, i
        elif context.peekToken(i) is not None \
                and context.peekToken(i).type in size_specifiers:
            i += 1
            i = self.skip_ws(context, i)
            if context.peekToken(i).type is not None \
                    and context.peekToken(i) in type_specifiers:
                return True, i
            return True, i
        elif context.peekToken(i) is not None \
                and (
                    context.peekToken(i).type in type_specifiers
                    or context.peekToken(i).type == "IDENTIFIER"):
            i += 1
            return True, i

        return False, pos

    def push_sub_parentheses(self, obj, depth, group):
        while depth > 0:
            group = group[-1]
            depth -= 1
        group.append(obj)

    def parse_parentheses(self, context, pos):
        i = pos
        groups = []
        depth = 0
        while context.peekToken(i) is not None \
                and context.peekToken(i).type != "OPENING_BRACKET" \
                and context.peekToken(i).type != "OP_SEMI_COLON":
            if context.peekToken(i).type == "OPENING_PARENTHESIS":
                self.push_sub_parentheses([], depth, groups)
                depth += 1
            elif context.peekToken(i).type == "CLOSING_PARENTHESIS":
                depth -= 1
            else:
                self.push_sub_parentheses(context.peekToken(i), depth, groups)
            i += 1
        return groups, i

    def innerleft_func_arguments(self, group):
        i = 0
        while i in range(len(group)):
            if isinstance(group[i], Token):
                if group[i].type in whitespaces \
                        or group[i].type in type_specifiers \
                        or group[i].type in misc_specifiers \
                        or group[i].type in sign_specifiers \
                        or group[i].type in size_specifiers \
                        or group[i].type in [
                            "OP_MULT",
                            "OP_COMMA",
                            "IDENTIFIER",
                            "CONSTANT",
                            "OP_ELLIPSIS",
                            "OPENING_SQUARE_BRACKET",
                            "CLOSING_SQUARE_BRACKET"]:
                    i += 1
                else:
                    return False
            elif isinstance(group[i], list):
                if group[i] == []:
                    i += 1
                    return True
                else:
                    ret = self.innerleft_func_arguments(group[i])
                    if ret is False:
                        return False
                    i += 1
        return True

    def innerleft_identifier(self, group, lvl=0):
        # False, False if no identifier is found
        # True, False if identifier is found but no function argument are found
        # True, True if identifier and func args are found in the same scope
        i = 0
        while i in range(len(group)):
            # print(group[i], i)
            if isinstance(group[i], Token):
                if group[i].type in whitespaces:
                    i += 1
                elif group[i].type == "OP_MULT":
                    i += 1
                elif group[i].type == "IDENTIFIER":
                    # now check if there is function arguments in this scope or
                    # sub scope
                    # print("in innerleft_identifier: ", group[i:])
                    i += 1
                    ret = self.innerleft_func_arguments(group[i:])
                    if ret is True:
                        return True, True
                    else:
                        return True, False
                else:
                    return False, False
            else:
                ret = self.innerleft_identifier(group[i])
                # print("ret is: ", ret)
                if ret[0] is True and ret[1] is True:
                    return True, True
                elif ret[0] is True and ret[0] is False:
                    i += 1
                    while i in range(len(group)):
                        if group[i] == []:
                            return True, True
                        else:
                            # print(group[i:])
                            ret = self.innerleft_func_arguments(group[i:])
                            if ret is True:
                                return True, ret
                else:
                    return False, False
        return False, False

    def check_func_prefix(self, context):
        i = self.skip_ws(context, 0)
        ret, i = self.check_functype_prefix(context, i)
        if ret is True:
            while context.peekToken(i) is not None \
                    and context.peekToken(i).type == "OP_MULT":
                i += 1
            return ret, i
        return False, 0

    def check_func_format(self, context):
        ret, i = self.check_func_prefix(context)
        if ret is False:
            return False, 0
        # print("1-- out of checkfuncprefix", ret, i, context.tokens[:i])
        i = self.skip_ws(context, i)
        # print("2-- out of skip_ws", ret, i, context.tokens[i])
        groups, i = self.parse_parentheses(context, i)
        # print("3-- groups from parse parenthese", groups, "tokens read->", i)
        ret = self.innerleft_identifier(groups)
        # print("4-- ret out of innerleft", ret)
        # print(ret)
        if ret[0] is True:
            # print(context.tokens[:i])
            if ret[1] is True:
                return ret, i
            else:
                ret = self.innerleft_func_arguments(groups)
                if ret is False:
                    return False, 0
                else:
                    return ret, i
        else:
            return False, 0

    def run(self, context):
        self.__i += 1
        ret, jump = self.check_func_format(context)
        if ret is False:
            return False, 0
        # print(context.tokens[:jump], '\n')
        for rulename in self.subrules:
            if rulename in context.rules:
                print(rulename)
        # Check for ';' or '{' in order to call for depending subrules
        if context.tokens[jump] == "OPENING_BRACKET":
            # FUNCTION BODY
            pass
        else:
            # FUNCTION PROTOTYPE
            pass
        return True, jump
