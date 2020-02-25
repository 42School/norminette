import unittest
import sys
from lexer.lexer import Lexer


def eat_tokens(line):
    lex = Lexer(line)
    line = ""
    while lex.get_next_token():
        line += lex.peek_token().test()
    return line


class TokensKeywordsTest(unittest.TestCase):

    def test_auto_keyword(self):
        self.assertEqual(eat_tokens("auto"), "<AUTO>")

    def test_break_keyword(self):
        self.assertEqual(eat_tokens("break"), "<BREAK>")

    def test_case_keyword(self):
        self.assertEqual(eat_tokens("case"), "<CASE>")

    def test_char_keyword(self):
        self.assertEqual(eat_tokens("char"), "<CHAR>")

    def test_const_keyword(self):
        self.assertEqual(eat_tokens("const"), "<CONST>")

    def test_continue_keyword(self):
        self.assertEqual(eat_tokens("continue"), "<CONTINUE>")

    def test_default_keyword(self):
        self.assertEqual(eat_tokens("default"), "<DEFAULT>")

    def test_do_keyword(self):
        self.assertEqual(eat_tokens("do"), "<DO>")

    def test_double_keyword(self):
        self.assertEqual(eat_tokens("double"), "<DOUBLE>")

    def test_else_keyword(self):
        self.assertEqual(eat_tokens("else"), "<ELSE>")

    def test_enum_keyword(self):
        self.assertEqual(eat_tokens("enum"), "<ENUM>")

    def test_extern_keyword(self):
        self.assertEqual(eat_tokens("extern"), "<EXTERN>")

    def test_float_keyword(self):
        self.assertEqual(eat_tokens("float"), "<FLOAT>")

    def test_for_keyword(self):
        self.assertEqual(eat_tokens("for"), "<FOR>")

    def test_goto_keyword(self):
        self.assertEqual(eat_tokens("goto"), "<GOTO>")

    def test_if_keyword(self):
        self.assertEqual(eat_tokens("if"), "<IF>")

    def test_int_keyword(self):
        self.assertEqual(eat_tokens("int"), "<INT>")

    def test_long_keyword(self):
        self.assertEqual(eat_tokens("long"), "<LONG>")

    def test_register_keyword(self):
        self.assertEqual(eat_tokens("register"), "<REGISTER>")

    def test_return_keyword(self):
        self.assertEqual(eat_tokens("return"), "<RETURN>")

    def test_signed_keyword(self):
        self.assertEqual(eat_tokens("signed"), "<SIGNED>")

    def test_sizeof_keyword(self):
        self.assertEqual(eat_tokens("sizeof"), "<SIZEOF>")

    def test_static_keyword(self):
        self.assertEqual(eat_tokens("static"), "<STATIC>")

    def test_struct_keyword(self):
        self.assertEqual(eat_tokens("struct"), "<STRUCT>")

    def test_switch_keyword(self):
        self.assertEqual(eat_tokens("switch"), "<SWITCH>")

    def test_typedef_keyword(self):
        self.assertEqual(eat_tokens("typedef"), "<TYPEDEF>")

    def test_union_keyword(self):
        self.assertEqual(eat_tokens("union"), "<UNION>")

    def test_unsigned_keyword(self):
        self.assertEqual(eat_tokens("unsigned"), "<UNSIGNED>")

    def test_void_keyword(self):
        self.assertEqual(eat_tokens("void"), "<VOID>")

    def test_volatile_keyword(self):
        self.assertEqual(eat_tokens("volatile"), "<VOLATILE>")

    def test_while_keyword(self):
        self.assertEqual(eat_tokens("while"), "<WHILE>")

    def test_define_keyword(self):
        self.assertEqual(eat_tokens("#define"), "<DEFINE=#define>")

    def test_error_keyword(self):
        self.assertEqual(eat_tokens("#error"), "<ERROR=#error>")

    def test_ifndef_keyword(self):
        self.assertEqual(eat_tokens("#ifndef"), "<IFNDEF=#ifndef>")

    def test_ifdef_keyword(self):
        self.assertEqual(eat_tokens("#ifdef"), "<IFDEF=#ifdef>")

    def test_include_keyword(self):
        self.assertEqual(eat_tokens("#include"), "<INCLUDE=#include>")

    def test_pragma_keyword(self):
        self.assertEqual(eat_tokens("#pragma"), "<PRAGMA=#pragma>")

    def test_undef_keyword(self):
        self.assertEqual(eat_tokens("#undef"), "<UNDEF=#undef>")


if __name__ == '__main__':
    unittest.main()
