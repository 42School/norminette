from lexer import Token
from rules import Rule

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
    "COMMA",
    "CLOSING_PARENTHESIS"
]


class CheckFuncArgumentsName(Rule):
    def skip_ws(self, context, pos):
        i = pos
        while context.peek_token(i) is not None \
                and context.peek_token(i).type in whitespaces:
            i += 1
        return i

    def skip_type_prefix(self, context, pos):
        i = pos
        i = self.skip_ws(context, i)

        if context.peek_token(i) is not None \
                and context.peek_token(i).type in misc_specifiers:
            # Skipping "const/register/struct/static/volatile" keywords
            i += 1
            i = self.skip_ws(context, i)

        if context.peek_token(i) is not None \
                and context.peek_token(i).type in sign_specifiers:
            # This case is the 'trickier'
            # sign specifier (signed, unsigned) can be followed by:
            # optionnal size specifier (long, short)
            # AND/OR optionnal type specifier (int, char)
            i += 1
            i = self.skip_ws(context, i)
            if context.peek_token(i) is not None \
                    and context.peek_token(i).type in size_specifiers:
                i += 1
                i = self.skip_ws(context, i)
                if context.peek_token(i) is not None \
                        and context.peek_token(i).type in type_specifiers:
                    i += 1
                    i = self.skip_ws(context, i)
                    return i
                return i

            else:
                return i
        elif context.peek_token(i) is not None \
                and context.peek_token(i).type in size_specifiers:
            i += 1
            i = self.skip_ws(context, i)
            if context.peek_token(i).type is not None \
                    and context.peek_token(i) in type_specifiers:
                return i
            return i
        else:
            i += 1
            return i

    def push_sub_parentheses(self, obj, depth, group):
        while depth > 0:
            group = group[-1]
            depth -= 1
        group.append(obj)

    def parse_parentheses(self, context, pos):
        i = pos
        groups = []
        depth = 0
        while context.peek_token(i) is not None \
                and context.peek_token(i).type != "LBRACE" \
                and context.peek_token(i).type != "SEMI_COLON":
            if context.peek_token(i).type == "LPARENTHESIS":
                self.push_sub_parentheses([], depth, groups)
                depth += 1
                #self.push_sub_parentheses(context.peek_token(i), depth, groups)
            elif context.peek_token(i).type == "RPARENTHESIS":
                depth -= 1
            elif context.peek_token(i).type not in whitespaces:
                self.push_sub_parentheses(context.peek_token(i), depth, groups)
            i += 1
        return groups, i

    def check_arg_format(self, context, group, pos):
        i = pos
        pass

    def check_args_format(self, context, group, pos):
        return
        if len(group) == 0:
            # how to get the position?????
            return
        self.check_arg_format(context, group, pos)
        # print(group)

    def check_sub_group(self, context, group):
        #print(group, len(group))
        if len(group) == 1 and isinstance(group[0], list):
            self.check_sub_group(context, group[0])
        else:
            i = 0
            self.check_args_format(context, group[-1], 0)
            #print('->',group,"\n", "-->",  group[-1])

    def run(self, context):
        return True, 0
        pos = self.skip_type_prefix(context, 0)
        pos = self.skip_ws(context, pos)
        # print(context.tokens[:context.tkn_scope])
        groups, pos = self.parse_parentheses(context, pos)
        #print(groups)
        # print(groups, "->",  groups[-1])
        self.check_sub_group(context, groups)
        print("\n")
        return False, 0
