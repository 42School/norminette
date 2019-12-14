import re
import string
from lexer.tokens import Token
from lexer.dictionary import keywords, operators, brackets


def read_file(filename):
    with open(filename) as f:
        return f.read()


class TokenError(Exception):
    def __init__(self, pos):
        self.msg = f"Unrecognized token line {pos[0]}, col {pos[1]}"

    def __repr__(self):
        return self.msg


class Lexer:
    def __init__(self, source_code):
        self.src = source_code
        self.len = len(source_code)
        self.__char = self.src[0] if self.src != "" else None
        self.__pos = int(0)
        self.__line_pos = int(1)
        self.__line = int(1)
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
            self.__line_pos = int((
                                self.__line_pos + 4 -
                                (self.__line_pos - 1) % 4) * 5 / 5)
        else:
            self.__line_pos += 1
        if self.__pos < self.len and self.src[self.__pos] == '\\':
            self.__pos += 1
        self.__pos += 1
        return self.peekChar()

    def peekToken(self):
        return self.tokens[-1]

    def linePos(self):
        return self.__line, self.__line_pos

    def isString(self):
        """
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
        """

        pos = self.linePos()
        tkn_value = ""
        bucket = ".0123456789aAbBcCdDeEfFlLuUxX-+"
        while self.peekChar() and self.peekChar() in bucket:
            if self.peekChar() in "xX":
                if tkn_value.startswith("0") is False or len(tkn_value) > 1:
                    raise TokenError(pos)
                for c in "xX":
                    if c in tkn_value:
                        raise TokenError(pos)

            elif self.peekChar() in "bB":
                if tkn_value != "0" \
                        and tkn_value.startswith("0x") is False \
                        and tkn_value.startswith("0X") is False:
                    raise TokenError(pos)

            elif self.peekChar() in "+-":
                if tkn_value.endswith("e") is False \
                        and tkn_value.endswith("E") is False \
                        or self.peekSubString(2) in ["++", "--"]:
                    break

            elif self.peekChar() in "eE" \
                    and "0x" not in tkn_value and "0X" not in tkn_value:
                if "e" in tkn_value or "E" in tkn_value \
                        or "f" in tkn_value or "F" in tkn_value \
                        or "u" in tkn_value or "U" in tkn_value \
                        or "l" in tkn_value or "L" in tkn_value:
                    raise TokenError(pos)

            elif self.peekChar() in "lL":
                lcount = tkn_value.count("l") + tkn_value.count("L")
                if lcount > 1 or (lcount == 1 and tkn_value[-1] not in "lL") \
                        or ("f" in tkn_value or "F" in tkn_value) \
                        and "0x" not in tkn_value and "0X" not in tkn_value:
                    raise TokenError(pos)
                elif self.peekChar() == 'l' and 'L' in tkn_value \
                        or self.peekChar() == 'L' and 'l' in tkn_value:
                    raise TokenError(pos)

            elif self.peekChar() in "uU":
                if "u" in tkn_value or "U" in tkn_value \
                        or (("e" in tkn_value or "E" in tkn_value
                            or "f" in tkn_value or "F" in tkn_value)
                            and (
                                "0x" not in tkn_value
                                and "0X" not in tkn_value)):
                    raise TokenError(pos)

            elif self.peekChar() in "Ff":
                if tkn_value.startswith("0x") is False \
                        and tkn_value.startswith("0X") is False \
                        and (
                            "." not in tkn_value
                            or "f" in tkn_value
                            or "F" in tkn_value) \
                        or "u" in tkn_value or "U" in tkn_value \
                        or "l" in tkn_value or "L" in tkn_value:
                    raise TokenError(pos)

            elif self.peekChar() in "aAbBcCdDeE" \
                    and tkn_value.startswith("0x") is False \
                    and tkn_value.startswith("0X") is False \
                    or "u" in tkn_value or "U" in tkn_value \
                    or "l" in tkn_value or "L" in tkn_value:
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
                self.__line_pos = 1
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
                self.popChar()
                self.__line_pos = 1
                self.__line += 1

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
