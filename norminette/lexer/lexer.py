import string
import pdb

from norminette.lexer.dictionary import brackets
from norminette.lexer.dictionary import keywords
from norminette.lexer.dictionary import operators
from norminette.lexer.dictionary import preproc_keywords
from norminette.lexer.tokens import Token


def read_file(filename):
    with open(filename) as f:
        return f.read()


class TokenError(Exception):
    def __init__(self, pos):
        self.msg = f"Error: Unrecognized token line {pos[0]}, col {pos[1]}"

    def __repr__(self):
        return self.msg


class Lexer:
    def __init__(self, source_code, starting_line=1):
        self.src = source_code
        self.len = len(source_code)
        self.__char = self.src[0] if self.src != "" else None
        self.__pos = int(0)
        self.__line_pos = int(starting_line)
        self.__line = int(starting_line)
        self.tokens = []

    def peek_sub_string(self, size):
        return self.src[self.__pos : self.__pos + size]

    def peek_char(self):
        """Return current character being checked,
        if the character is a backslash character the following
        character is appended to the return value. It will allow us to
        parse escaped characters easier.
        """
        if self.__pos < self.len:
            if self.src[self.__pos] == "\\":
                self.__char = self.src[self.__pos : self.__pos + 2]
            else:
                self.__char = self.src[self.__pos]
        else:
            self.__char = None
        return self.__char

    def pop_char(self):
        """Pop a character that's been read by increasing self.__pos,
        for escaped characters self.__pos will be increased twice
        """
        if self.peek_char() == "\t":
            # this calculates the 'visual offset' of a tab based on it's
            # position on the line, if there's an easier way to calculate this
            # you're welcome
            self.__line_pos = int((self.__line_pos + 4 - (self.__line_pos - 1) % 4) * 5 / 5)
        else:
            self.__line_pos += 1
        if self.__pos < self.len and self.src[self.__pos] == "\\":
            self.__pos += 1
        self.__pos += 1
        return self.peek_char()

    def peek_token(self):
        return self.tokens[-1]

    def line_pos(self):
        return self.__line, self.__line_pos

    def is_string(self):
        """True if current character could start a string constant"""
        if self.peek_sub_string(2) == 'L"' or self.peek_char() == '"':
            return True
        else:
            return False

    def is_constant(self):
        """True if current character could start a numeric constant"""
        if self.peek_char() in string.digits:
            return True
        elif self.peek_char() == ".":
            for i in range(0, self.len - self.__pos):
                if self.src[self.__pos + i] == ".":
                    i += 1
                elif self.src[self.__pos + i] in "0123456789":
                    return True
                else:
                    return False
        else:
            return False

    def is_char_constant(self):
        """True if current character could start a character constant"""
        if self.peek_char() == "'" or self.peek_sub_string(2) == "L'":
            return True
        else:
            return False

    def string(self):
        """String constants can contain any characer except unescaped newlines.
        An unclosed string or unescaped newline is a fatal error and thus
        parsing will stop here.
        """
        pos = self.line_pos()
        tkn_value = ""
        if self.peek_char() == "L":
            tkn_value += self.peek_char()
            self.pop_char()
        tkn_value += self.peek_char()
        self.pop_char()
        while self.peek_char() not in [None]:
            tkn_value += self.peek_char()
            if self.peek_sub_string(2) == "\\\n":
                self.__line += 1
                self.__line_pos = 1
            if self.peek_char() == '"':
                break
            self.pop_char()
        else:
            raise TokenError(pos)
            return
        self.tokens.append(Token("STRING", pos, tkn_value))
        self.pop_char()

    def char_constant(self):
        """Char constants follow pretty much the same rule as string constants"""
        pos = self.line_pos()
        tkn_value = "'"
        self.pop_char()
        while self.peek_char():
            tkn_value += self.peek_char()
            if self.peek_char() == "\n":
                self.pop_char()
                self.tokens.append(Token("TKN_ERROR", pos))
                return
            if self.peek_char() == "'":
                for i in tkn_value:
                    if i == '\\':
                        self.__line_pos += 1
                self.pop_char()
                self.tokens.append(Token("CHAR_CONST", pos, tkn_value))
                return
            self.pop_char()
        raise TokenError(pos)

    def constant(self):
        """Numeric constants can take many forms:
        - integer constants only allow digits [0-9]
        - real number constant only allow digits [0-9],
            ONE optionnal dot '.' and ONE optionnal 'e/E' character
        - binary constant only allow digits [0-1] prefixed by '0b' or '0B'
        - hex constant only allow digits [0-9], letters [a-f/A-F] prefixed
            by '0x' or '0X'
        - octal constants allow digits [0-9] prefixed by a zero '0'
            character

        Size ('l/L' for long) and sign ('u/U' for unsigned) specifiers can
        be appended to any of those. tokens

        Plus/minus operators ('+'/'-') can prefix any of those tokens

        a numeric constant could start with a '.' (dot character)
        """
        pos = self.line_pos()
        tkn_value = ""
        bucket = ".0123456789aAbBcCdDeEfFlLuUxX-+"
        while self.peek_char() and (self.peek_char() in bucket or self.peek_char() == "\\\n"):
            if self.peek_char() in "xX":
                if tkn_value.startswith("0") is False or len(tkn_value) > 1:
                    raise TokenError(pos)
                for c in "xX":
                    if c in tkn_value:
                        raise TokenError(pos)

            elif self.peek_char() in "bB":
                if tkn_value != "0" and tkn_value.startswith("0x") is False and tkn_value.startswith("0X") is False:
                    raise TokenError(pos)

            elif self.peek_char() in "+-":
                if (
                    tkn_value.endswith("e") is False
                    and tkn_value.endswith("E") is False
                    or self.peek_sub_string(2) in ["++", "--"]
                ):
                    break

            elif self.peek_char() in "eE" and "0x" not in tkn_value and "0X" not in tkn_value:
                if (
                    "e" in tkn_value
                    or "E" in tkn_value
                    or "f" in tkn_value
                    or "F" in tkn_value
                    or "u" in tkn_value
                    or "U" in tkn_value
                    or "l" in tkn_value
                    or "L" in tkn_value
                ):
                    raise TokenError(pos)

            elif self.peek_char() in "lL":
                lcount = tkn_value.count("l") + tkn_value.count("L")
                if (
                    lcount > 1
                    or (lcount == 1 and tkn_value[-1] not in "lL")
                    or ("f" in tkn_value or "F" in tkn_value)
                    and "0x" not in tkn_value
                    and "0X" not in tkn_value
                ):
                    raise TokenError(pos)
                elif self.peek_char() == "l" and "L" in tkn_value or self.peek_char() == "L" and "l" in tkn_value:
                    raise TokenError(pos)

            elif self.peek_char() in "uU":
                if (
                    "u" in tkn_value
                    or "U" in tkn_value
                    or (
                        ("e" in tkn_value or "E" in tkn_value or "f" in tkn_value or "F" in tkn_value)
                        and ("0x" not in tkn_value and "0X" not in tkn_value)
                    )
                ):
                    raise TokenError(pos)

            elif self.peek_char() in "Ff":
                if (
                    tkn_value.startswith("0x") is False
                    and tkn_value.startswith("0X") is False
                    and ("." not in tkn_value or "f" in tkn_value or "F" in tkn_value)
                    or "u" in tkn_value
                    or "U" in tkn_value
                    or "l" in tkn_value
                    or "L" in tkn_value
                ):
                    raise TokenError(pos)

            elif (
                self.peek_char() in "aAbBcCdDeE"
                and tkn_value.startswith("0x") is False
                and tkn_value.startswith("0X") is False
                or "u" in tkn_value
                or "U" in tkn_value
                or "l" in tkn_value
                or "L" in tkn_value
            ):
                raise TokenError(pos)

            elif (
                self.peek_char() in "0123456789"
                and "u" in tkn_value
                or "U" in tkn_value
                or "l" in tkn_value
                or "L" in tkn_value
            ):
                raise TokenError(pos)

            elif self.peek_char() == "." and "." in tkn_value:
                raise TokenError(pos)

            tkn_value += self.peek_char()
            self.pop_char()
        if tkn_value[-1] in "eE" and tkn_value.startswith("0x") is False or tkn_value[-1] in "xX":
            raise TokenError(pos)
        else:
            self.tokens.append(Token("CONSTANT", pos, tkn_value))

    def mult_comment(self):
        pos = self.line_pos()
        self.pop_char(), self.pop_char()
        tkn_value = "/*"
        while self.peek_char():
            if self.src[self.__pos :].startswith("*/"):
                tkn_value += "*/"
                self.pop_char(), self.pop_char()
                break
            tkn_value += self.peek_char()
            if self.peek_char() == "\n":
                self.__line += 1
                self.__line_pos = 1
            self.pop_char()
        if tkn_value.endswith("*/"):
            self.tokens.append(Token("MULT_COMMENT", pos, tkn_value))
        else:
            raise TokenError(pos)

    def comment(self):
        """Comments are anything after '//' characters, up until a newline or
        end of file
        """
        pos = self.line_pos()
        tkn_value = "//"
        self.pop_char(), self.pop_char()
        while self.peek_char() is not None:
            if self.peek_char() == "\n":
                self.tokens.append(Token("COMMENT", pos, tkn_value))
                return
            tkn_value += self.peek_char()
            self.pop_char()
        if (self.__pos == self.len):
            self.tokens.append(Token("COMMENT", pos, tkn_value))
            return
        raise TokenError(pos)

    def identifier(self):
        """Identifiers can start with any letter [a-z][A-Z] or an underscore
        and contain any letters [a-z][A-Z] digits [0-9] or underscores
        """
        pos = self.line_pos()
        tkn_value = ""
        while self.peek_char() and (
            self.peek_char() in string.ascii_letters + "0123456789_" or self.peek_char() == "\\\n"
        ):
            if self.peek_char() == "\\\n":
                self.pop_char()
                continue
            tkn_value += self.peek_char()
            self.pop_char()
        if tkn_value in keywords:
            self.tokens.append(Token(keywords[tkn_value], pos))

        else:
            self.tokens.append(Token("IDENTIFIER", pos, tkn_value))

    def operator(self):
        """Operators can be made of one or more sign, so the longest operators
        need to be looked up for first in order to avoid false positives
        eg: '>>' being understood as two 'MORE_THAN' operators instead of
            one 'RIGHT_SHIFT' operator
        """
        pos = self.line_pos()
        if self.peek_char() in ".+-*/%<>^&|!=":

            if self.peek_sub_string(3) in [">>=", "<<=", "..."]:
                self.tokens.append(Token(operators[self.peek_sub_string(3)], pos))
                self.pop_char(), self.pop_char(), self.pop_char()

            elif self.peek_sub_string(2) in [">>", "<<", "->"]:
                self.tokens.append(Token(operators[self.peek_sub_string(2)], pos))
                self.pop_char(), self.pop_char()

            elif self.peek_sub_string(2) == self.peek_char() + "=":
                self.tokens.append(Token(operators[self.peek_sub_string(2)], pos))
                self.pop_char(), self.pop_char()

            elif self.peek_char() in "+-<>=&|":
                if self.peek_sub_string(2) == self.peek_char() * 2:
                    self.tokens.append(Token(operators[self.peek_sub_string(2)], pos))
                    self.pop_char()
                    self.pop_char()

                else:
                    self.tokens.append(Token(operators[self.peek_char()], pos))
                    self.pop_char()

            else:
                self.tokens.append(Token(operators[self.peek_char()], pos))
                self.pop_char()

        else:
            self.tokens.append(Token(operators[self.src[self.__pos]], pos))
            self.pop_char()

    def preprocessor(self):
        pos = self.line_pos()
        tkn_value = ""
        while self.peek_char():
            tkn_value += self.peek_char()
            self.pop_char()
            if self.peek_sub_string(2) == "\\\n":
                self.__line_pos = 1
                self.__line += 1
            #    raise TokenError(self.line_pos())
            if self.peek_sub_string(2) in ["//", "/*"] or self.peek_char() == "\n":
                break
        if len(tkn_value) <= 1:
            raise TokenError(self.line_pos())
        tkn_key = tkn_value[1:].split()[0]
        if tkn_key not in preproc_keywords and tkn_key[: len("include")] != "include":
            raise TokenError(self.line_pos())
        else:
            if tkn_key not in preproc_keywords and tkn_key[: len("include")] == "include":
                tkn_key = "include"
            self.tokens.append(Token(preproc_keywords.get(tkn_key), pos, tkn_value))

    def get_next_token(self):
        """Peeks one character and tries to match it to a token type,
        if it doesn't match any of the token types, an error will be raised
        and current file's parsing will stop
        """
        while self.peek_char() is not None:
            if self.is_string():
                self.string()

            elif (self.peek_char().isalpha() and self.peek_char().isascii()) or self.peek_char() == "_":
                self.identifier()

            elif self.is_constant():
                self.constant()

            elif self.is_char_constant():
                self.char_constant()

            elif self.peek_char() == "#":
                self.preprocessor()

            elif self.src[self.__pos :].startswith("/*"):
                self.mult_comment()

            elif self.src[self.__pos :].startswith("//"):
                self.comment()

            elif self.peek_char() in "+-*/,<>^&|!=%;:.~?":
                self.operator()

            elif self.peek_char() == " ":
                self.tokens.append(Token("SPACE", self.line_pos()))
                self.pop_char()

            elif self.peek_char() == "\t":
                self.tokens.append(Token("TAB", self.line_pos()))
                self.pop_char()

            elif self.peek_char() == "\n":  # or ord(self.peek_char()) == 8203:
                self.tokens.append(Token("NEWLINE", self.line_pos()))
                self.pop_char()
                self.__line_pos = 1
                self.__line += 1

            elif self.peek_char() == "\\\n":
                self.tokens.append(Token("ESCAPED_NEWLINE", self.line_pos()))
                self.pop_char()
                self.__line_pos = 1
                self.__line += 1

            elif self.peek_char() in brackets:
                self.tokens.append(Token(brackets[self.peek_char()], self.line_pos()))
                self.pop_char()
            else:
                raise TokenError(self.line_pos())

            return self.peek_token()

        return None

    def get_tokens(self):
        """Iterate through self.get_next_token() to convert source code into a
        token list
        """
        while self.get_next_token():
            continue
        return self.tokens

    def print_tokens(self):
        if self.tokens == []:
            return
        for t in self.tokens:
            if t.type == "NEWLINE":
                print(t)
            else:
                print(t, end="")
        if self.tokens[-1].type != "NEWLINE":
            print("")

    def check_tokens(self):
        """
        Only used for testing
        """
        if self.tokens == []:
            self.get_tokens()
            if self.tokens == []:
                return ""
        ret = ""
        for i in range(0, len(self.tokens)):
            ret += self.tokens[i].test()
            ret += "" if self.tokens[i].type != "NEWLINE" else "\n"
        if self.tokens[-1].type != "NEWLINE":
            ret += "\n"
        return ret
