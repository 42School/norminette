from .norm_error import NormError

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


class CheckFuncDeclarations:
    def __init__(self):
        self.name = "CheckFuncDeclaration"

    def skip_ws(self, tokens, pos):
        i = 0
        while tokens[pos + i].type in ["SPACE", "TAB"]:
            i += 1
        return i

    def check_type_prefix(self, tokens, pos):
        i = pos
        i += self.skip_ws(tokens, i)

        if tokens[i].type in misc_specifiers:
            i += 1
            i += self.skip_ws(tokens, i)

        if tokens[i].type in sign_specifiers:
            # sign specifier (signed, unsigned) can be followed by:
            # optionnal size specifier (long, short)
            # optionnal type specifier (int, char, double, float, etc)
            i += 1
            i += self.skip_ws(tokens, i)
            if tokens[i].type in size_specifiers:
                i += 1
                i += self.skip_ws(tokens, i)
                if tokens[i].type in type_specifiers:
                    i += 1
                    return True, i
                return True, i

            else:
                i += 1
                return True, i

        elif tokens[i].type in size_specifiers:
            i += 1
            i += self.skip_ws(tokens, i)
            if tokens[i].type in type_specifiers:
                i += 1
                j = i
                j = self.skip_ws(tokens, j)
                if tokens[j] in ["CLOSING_PARENTHESIS", "OP_COMMA"]:
                    #append error 1002 to context
                    pass
                return True, i
            return True, i

        elif tokens[i].type in type_specifiers \
                or tokens[i].type == "IDENTIFIER":
            i += 1
            return True, i

        return False, pos

    def check_func_pointer_args(self, tokens, pos):
        i = pos
        i += self.skip_ws(tokens, i)
        count = 0
        while tokens[i].type == "OPENING_PARENTHESIS":
            i += 1
            count += 1
        while True:
            i += self.skip_ws(tokens, i)
            ret, i = self.check_type_prefix(tokens, i)
            print("THERE", ret, i, tokens[i:])
            if ret is True:
                if tokens[i].type == "OP_COMMA":
                    i += 1
                    continue
                i += self.skip_ws(tokens, i)
                if tokens[i].type not in ["OP_COMMA", "CLOSING_PARENTHESIS"]:
                    ret, i = self.check_var_format(tokens, i)
                    if ret is False:
                        return False, pos

            elif tokens[i].type == "OPENING_PARENTHESIS":
                ret, i = self.check_func_pointer_args(tokens, i)

            elif tokens[i].type == "CLOSING_PARENTHESIS": break

            else: return False, pos

        while tokens[i].type == "CLOSING_PARENTHESIS" and count > 0:
            i += 1
            count -= 1
        return (True, i) if count == 0 else (False, pos)

    def check_var_format(self, tokens, pos):
        i = pos
        i += self.skip_ws(tokens, i)
        while tokens[i].type == "OP_MULT":
            i += 1
        i += self.skip_ws(tokens, i)

        if tokens[i].type == "IDENTIFIER":
            i += 1
            return True, i

        elif tokens[i].type == "OPENING_PARENTHESIS":
            # This MIGHT be a function pointer
            count = 0
            while tokens[i].type == "OPENING_PARENTHESIS":
                i +=  1
                count += 1
            while tokens[i].type == "OP_MULT":
                i += 1

            if tokens[i].type == "IDENTIFIER":
                print(tokens[i])
                i += 1
                if tokens[i].type == "OPENING_PARENTHESIS":
                    print("HERE")
                    ret, i = self.check_func_pointer_args(tokens, i)
                    print(ret, i)
                    if ret is False:
                        return False, pos
                while tokens[i].type == "CLOSING_PARENTHESIS" and count > 0:
                    i += 1
                    count -= 1
                if count != 0:
                    return False, pos
                return True, i

        return False, pos

    def count_extra_func_args(self, tokens, pos):
        return 0

    def check_func_args(self, tokens, pos):
        i = pos
        i += self.skip_ws(tokens, i)
        arg_count = 0
        par_count = 0
        while tokens[i].type == "OPENING_PARENTHESIS":
            i += 1
            par_count += 1
        i += self.skip_ws(tokens, i)
        ret, jump = self.check_var_format
        if ret is False:
            return False, pos
        else:
            arg_count += 1

    def check_return_type(self, tokens, pos):
        pass

    def run(self, tokens):
        ret, jump = self.check_type_prefix(tokens, 0)
        print(ret, jump,  tokens[jump:])
        if ret is True:
            ret, jump = self.check_var_format(tokens, jump)
            if ret is True:
                print(ret, jump, tokens[jump:])
                return True,jump
            return False
        return ret
