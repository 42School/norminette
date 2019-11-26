import unittest
import sys
from lexer import Lexer


sys.path.append('../..')

def eat_tokens(line):
    lex = Lexer(line)
    line = ""
    while lex.getNextToken():
        line += lex.peekToken().test()
        if lex.peekToken().type in ["EOF", "ERROR"]:
            break
    return line


class TokensKeywordsTest(unittest.TestCase):

    def test_auto_keyword(self):
        self.assertEqual(eat_tokens("auto"), "<AUTO><EOF>")

    def test_break_keyword(self):
        self.assertEqual(eat_tokens("break"), "<BREAK><EOF>")

    def test_case_keyword(self):
        self.assertEqual(eat_tokens("case"), "<CASE><EOF>")

    def test_char_keyword(self):
        self.assertEqual(eat_tokens("char"), "<CHAR><EOF>")

    def test_const_keyword(self):
        self.assertEqual(eat_tokens("const"), "<CONST><EOF>")

    def test_continue_keyword(self):
        self.assertEqual(eat_tokens("continue"), "<CONTINUE><EOF>")

    def test_default_keyword(self):
        self.assertEqual(eat_tokens("default"), "<DEFAULT><EOF>")

    def test_do_keyword(self):
        self.assertEqual(eat_tokens("do"), "<DO><EOF>")

    def test_double_keyword(self):
        self.assertEqual(eat_tokens("double"), "<DOUBLE><EOF>")

    def test_else_keyword(self):
        self.assertEqual(eat_tokens("else"), "<ELSE><EOF>")

    def test_enum_keyword(self):
        self.assertEqual(eat_tokens("enum"), "<ENUM><EOF>")

    def test_extern_keyword(self):
        self.assertEqual(eat_tokens("extern"), "<EXTERN><EOF>")

    def test_float_keyword(self):
        self.assertEqual(eat_tokens("float"), "<FLOAT><EOF>")

    def test_for_keyword(self):
        self.assertEqual(eat_tokens("for"), "<FOR><EOF>")

    def test_goto_keyword(self):
        self.assertEqual(eat_tokens("goto"), "<GOTO><EOF>")

    def test_if_keyword(self):
        self.assertEqual(eat_tokens("if"), "<IF><EOF>")

    def test_int_keyword(self):
        self.assertEqual(eat_tokens("int"), "<INT><EOF>")

    def test_long_keyword(self):
        self.assertEqual(eat_tokens("long"), "<LONG><EOF>")

    def test_register_keyword(self):
        self.assertEqual(eat_tokens("register"), "<REGISTER><EOF>")

    def test_return_keyword(self):
        self.assertEqual(eat_tokens("return"), "<RETURN><EOF>")

    def test_signed_keyword(self):
        self.assertEqual(eat_tokens("signed"), "<SIGNED><EOF>")

    def test_sizeof_keyword(self):
        self.assertEqual(eat_tokens("sizeof"), "<SIZEOF><EOF>")

    def test_static_keyword(self):
        self.assertEqual(eat_tokens("static"), "<STATIC><EOF>")

    def test_struct_keyword(self):
        self.assertEqual(eat_tokens("struct"), "<STRUCT><EOF>")

    def test_switch_keyword(self):
        self.assertEqual(eat_tokens("switch"), "<SWITCH><EOF>")

    def test_typedef_keyword(self):
        self.assertEqual(eat_tokens("typedef"), "<TYPEDEF><EOF>")

    def test_union_keyword(self):
        self.assertEqual(eat_tokens("union"), "<UNION><EOF>")

    def test_unsigned_keyword(self):
        self.assertEqual(eat_tokens("unsigned"), "<UNSIGNED><EOF>")

    def test_void_keyword(self):
        self.assertEqual(eat_tokens("void"), "<VOID><EOF>")

    def test_volatile_keyword(self):
        self.assertEqual(eat_tokens("volatile"), "<VOLATILE><EOF>")

    def test_while_keyword(self):
        self.assertEqual(eat_tokens("while"), "<WHILE><EOF>")

    def test_define_keyword(self):
        self.assertEqual(eat_tokens("define"), "<DEFINE><EOF>")

    def test_error_keyword(self):
        self.assertEqual(eat_tokens("error"), "<ERROR><EOF>")

    def test_ifndef_keyword(self):
        self.assertEqual(eat_tokens("ifndef"), "<IFNDEF><EOF>")

    def test_ifdef_keyword(self):
        self.assertEqual(eat_tokens("ifdef"), "<IFDEF><EOF>")

    def test_include_keyword(self):
        self.assertEqual(eat_tokens("include"), "<INCLUDE><EOF>")

    def test_pragma_keyword(self):
        self.assertEqual(eat_tokens("pragma"), "<PRAGMA><EOF>")

    def test_undef_keyword(self):
        self.assertEqual(eat_tokens("undef"), "<UNDEF><EOF>")


if __name__ == '__main__':
    unittest.main()
