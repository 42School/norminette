import re
import string
from tokens import Token
from dictionary import keywords, operators, brackets


def read_file(filename):
    with open(filename) as f:
        return f.read()


class TokenError(Exception):
    def __init__(self, pos):
        self.pos = pos
        self.err = f"Unexpected token line {pos[0]}, col {pos[1]}"


class Lexer:
    def __init__(self, source_code):
        self.src = source_code
        self.len = len(source_code)
        self.__char = self.src[0] if self.src != "" else None
        self.__pos = 0
        self.__line_pos = 1
        self.__line = 1
        self.tokens = []

    def peekSubString(self, size):
        return self.src[self.__pos: self.__pos + size]

    def peekChar(self):
        if self.__pos < self.len:
            if self.src[self.__pos] == '\\':
                self.__char = self.src[self.__pos:self.__pos + 2]
            else:
                self.__char = self.src[self.__pos]
        else:
            self.__char = None

        return self.__char

    def popChar(self):
        if self.peekChar() == "\t":
            self.__line_pos += 3
        if self.__pos < self.len and self.src[self.__pos] == '\\':
            self.__pos += 1
        self.__pos += 1
        self.__line_pos += 1
        return self.peekChar()

    def peekToken(self):
        return self.tokens[-1]

    def linePos(self):
        return self.__line, self.__line_pos

    def isString(self):
        """
        Strings can start either with `"` (one double quote character)
        or `L"` (an `L` immediatly followed by a double quote character).
        """
        if self.peekSubString(2) == 'L"' or self.peekChar() == '"':
            return True
        else:
            return False

    def isConstant(self):
        if self.peekChar() in string.digits:
            return True
        elif self.peekChar() == ".":
            for i in range(0, self.len - self.__pos):
                if self.src[self.__pos + i] == ".":
                    i += 1
                elif self.src[self.__pos + i] in "0123456789":
                    return True
                else:
                    return False
        else:
            return False

    def isCharConstant(self):
        if self.peekChar() == '\'' or self.peekSubString(2) == "L'":
            return True
        else:
            return False

    def string(self):
        """
        If the string has no closing quote character, it is not properly
        formatted and we most likely won't be able to make sense of the file's
        content from here on. We'll stop parsing  here and send back an
        TKN_ERROR token
        """
        pos = self.linePos()
        tkn_value = ""
        if self.peekChar() == 'L':
            tkn_value += self.peekChar()
            self.popChar()
        tkn_value += self.peekChar()
        self.popChar()
        while self.peekChar() not in ["\"", "\n", None]:
            tkn_value += self.peekChar()
            self.popChar()
        tkn_value += self.peekChar() if self.peekChar() is not None else ""
        if self.peekChar() in ["\n", None]:
            raise TokenError(pos)
        else:
            self.tokens.append(Token("STRING", pos, tkn_value))
        self.popChar()
        pass

    def constant(self):
        """
        Constant can be either:
        -Integer (0, 1, etc)
        -Octal (00, 01, etc)
        -Hexadecimal (0x0, 0x1, etc)
        Hexadecimals constants only allow one 'X' or 'x'.
        Real numbers cam only contain one 'E' or 'e'
        """
        pos = self.linePos()
        sign = None
        tkn_value = ""
        bucket = ".0123456789aAbBcCdDeEfFlLuUxX"
        while self.peekChar() and self.peekChar() in bucket:
            if self.peekChar() in "xX":
                if tkn_value.startswith("0") is False or len(tkn_value) > 1:
                    self.tokens.append(Token("TKN_ERROR", pos))
                    return
                for c in "xX":
                    if c in tkn_value:
                        raise TokenError(pos)

            elif self.peekChar() in "eE" \
                    and "x" not in tkn_value and "X" not in tkn_value:
                for c in "eE":
                    if c in tkn_value:
                        raise TokenError(pos)

            elif self.peekChar() in "lL":
                lcount = tkn_value.count("l") + tkn_value.count("L")
                if lcount > 1 or (lcount == 1 and tkn_value[-1] not in "lL") \
                        or "e" in tkn_value or "E" in tkn_value:
                    raise TokenError(pos)

            elif self.peekChar() in "uU":
                if "u" in tkn_value or "U" in tkn_value \
                        or "e" in tkn_value or "E" in tkn_value:
                    raise TokenError(pos)

            elif self.peekChar() in "aAbBcCdDeEfF" \
                    and tkn_value.startswith("0x") is False \
                    and tkn_value.startswith("0X") is False:
                raise TokenError(pos)

            elif self.peekChar() in "0123456789" \
                    and "u" in tkn_value or "U" in tkn_value \
                    or "l" in tkn_value or "L" in tkn_value:
                raise TokenError(pos)

            elif self.peekChar() == '.' and '.' in tkn_value:
                raise TokenError(pos)

            tkn_value += self.peekChar()
            self.popChar()
        if tkn_value[-1] in "eE" and tkn_value.startswith("0x") is False \
                or tkn_value[-1] in "xX":
            raise TokenError(pos)
        else:
            self.tokens.append(Token(
                                    "CONSTANT",
                                    pos,
                                    tkn_value))

    def charConstant(self):
        pos = self.linePos()
        tkn_value = '\''
        self.popChar()
        while self.peekChar():
            tkn_value += self.peekChar()
            if self.peekChar() == '\n':
                self.popChar()
                self.tokens.append(Token("TKN_ERROR", pos))
                return
            if self.peekChar() == '\'':
                self.popChar()
                self.tokens.append(Token(
                                        "CHAR_CONST",
                                        pos,
                                        tkn_value))
                return
            self.popChar()
        raise TokenError(pos)

    def multComment(self):
        pos = self.linePos()
        self.popChar(), self.popChar()
        tkn_value = "/*"
        while self.peekChar():
            tkn_value += self.peekChar()
            if self.peekChar() == '\n':
                self.__line += 1
                self.__line_pos = 0
            self.popChar()
            if self.src[self.__pos:].startswith("*/"):
                tkn_value += "*/"
                self.popChar(), self.popChar()
                break
        if tkn_value.endswith("*/"):
            self.tokens.append(Token(
                                    "MULT_COMMENT",
                                    pos,
                                    tkn_value))
        else:
            raise TokenError(pos)

    def comment(self):
        pos = self.linePos()
        tkn_value = "//"
        self.popChar(), self.popChar()
        while self.peekChar():
            if self.peekChar() == '\n':
                self.tokens.append(Token("COMMENT", pos, tkn_value))
                return
            tkn_value += self.peekChar()
            self.popChar()
        raise TokenError(pos)

    def identifier(self):
        pos = self.linePos()
        tkn_value = ""
        while self.peekChar() \
                and self.peekChar() in string.ascii_letters + "0123456789_":
            tkn_value += self.peekChar()
            self.popChar()
        if tkn_value in keywords:
            self.tokens.append(Token(
                            keywords[tkn_value],
                            pos))
        else:
            self.tokens.append(Token(
                            "IDENTIFIER",
                            pos,
                            tkn_value))

    def operator(self):
        pos = self.linePos()
        if self.peekChar() in ".+-*/%<>^&|!=":
            if self.peekSubString(3) in [">>=", "<<=", "..."]:
                self.tokens.append(Token(
                            operators[self.peekSubString(3)],
                            pos))
                self.__pos += 3
            elif self.peekSubString(2) in [">>", "<<", "->"]:
                self.tokens.append(Token(
                            operators[self.peekSubString(2)],
                            pos))
                self.__pos += 2
            elif self.peekSubString(2) == self.peekChar() + "=":
                self.tokens.append(Token(
                            operators[self.peekSubString(2)],
                            pos))
                self.popChar(), self.popChar()
            elif self.peekChar() in "+-<>=&|":
                if self.peekSubString(2) == self.peekChar() * 2:
                    self.tokens.append(Token(
                                operators[self.peekSubString(2)],
                                pos))
                    self.popChar()
                    self.popChar()
                else:
                    self.tokens.append(Token(
                                operators[self.peekChar()], pos))
                    self.popChar()
            else:
                self.tokens.append(Token(
                        operators[self.peekChar()],
                        pos))
                self.popChar()
        else:
            self.tokens.append(Token(
                    operators[self.src[self.__pos]],
                    pos))
            self.popChar()

    def preprocessor(self):
        pos = self.linePos()
        tkn_value = ""
        while self.peekChar():
            tkn_value += self.peekChar()
            self.popChar()
            if self.peekSubString(2) in ["//", "/*"] \
                    or self.peekChar() == '\n':
                self.tokens.append(Token("PREPROC", pos, tkn_value))
                return

    def getNextToken(self):
        """
        This method creates and return 1 token at a time by reading the source
        code character after character and matching a character or set of
        characters to a pattern related to a token type.
        If no pattern matches the current character or set of character, an
        "TKN_ERROR" token will be returned.
        After reading the whole file, an "EOF" token is returned
        """
        while self.peekChar() is not None:

            if self.isString():
                self.string()

            elif self.peekChar().isalpha() or self.peekChar() == '_':
                self.identifier()

            elif self.isConstant():
                self.constant()

            elif self.isCharConstant():
                self.charConstant()

            elif self.peekChar() == '#':
                self.preprocessor()

            elif self.src[self.__pos:].startswith("/*"):
                self.multComment()

            elif self.src[self.__pos:].startswith("//"):
                self.comment()

            elif self.peekChar() in "+-*/,<>^&|!=%;:.~?":
                self.operator()

            elif self.peekChar() == ' ':
                self.tokens.append(Token("SPACE", self.linePos()))
                self.popChar()

            elif self.peekChar() == '\t':
                self.tokens.append(Token("TAB", self.linePos()))
                self.popChar()

            elif self.peekChar() in ['\n', '\\\n']:
                self.tokens.append(Token("NEWLINE", self.linePos()))
                self.__line_pos = 0
                self.__line += 1
                self.popChar()

            elif self.peekChar() in brackets:
                self.tokens.append(Token(
                                    brackets[self.peekChar()],
                                    self.linePos()))
                self.popChar()

            else:
                raise TokenError(self.linePos())

            return self.peekToken()

        return None

    def getTokens(self):
        while self.getNextToken():
            continue
        return self.tokens

    def checkTokens(self):
        """
        This function is only used for testing
        """
        if self.tokens == []:
            self.getTokens()
            if self.tokens == []:
                return ""
        ret = ""
        for i in range(0, len(self.tokens)):
            ret += self.tokens[i].test()
            ret += "" if self.tokens[i].type != "NEWLINE" else "\n"
        if self.tokens[-1].type != "NEWLINE":
            ret += "\n"
        return ret
