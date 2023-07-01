import unittest

from norminette.lexer.lexer import Lexer


def eat_tokens(line):
    lex = Lexer(line)
    tokens = []
    while lex.get_next_token():
        tokens.append(lex.peek_token().test())
    if len(tokens) == 1:
        return tokens[0]
    return tokens


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
        self.assertEqual(eat_tokens("#define"), ["<HASH>", "<IDENTIFIER=define>"])
        self.assertEqual(eat_tokens("# define "), ["<HASH>", "<SPACE>", "<IDENTIFIER=define>", "<SPACE>"])
        self.assertEqual(eat_tokens("#define 	"), ["<HASH>", "<IDENTIFIER=define>", "<SPACE>", "<TAB>"])
        self.assertEqual(eat_tokens("#define //bla"), ["<HASH>", "<IDENTIFIER=define>", "<SPACE>", "<COMMENT=//bla>"])
        self.assertEqual(eat_tokens("#define//bla "), ["<HASH>", "<IDENTIFIER=define>", "<COMMENT=//bla >"])

    def test_error_keyword(self):
        self.assertEqual(eat_tokens("#error"), ["<HASH>", "<IDENTIFIER=error>"])
        self.assertEqual(eat_tokens("# error "), ["<HASH>", "<SPACE>", "<IDENTIFIER=error>", "<SPACE>"])
        self.assertEqual(eat_tokens("#error 	"), ["<HASH>", "<IDENTIFIER=error>", "<SPACE>", "<TAB>"])
        self.assertEqual(eat_tokens("#error //bla"), ["<HASH>", "<IDENTIFIER=error>", "<SPACE>", "<COMMENT=//bla>"])
        self.assertEqual(eat_tokens("#error//bla "), ["<HASH>", "<IDENTIFIER=error>", "<COMMENT=//bla >"])

    def test_ifndef_keyword(self):
        self.assertEqual(eat_tokens("#ifndef"), ["<HASH>", "<IDENTIFIER=ifndef>"])
        self.assertEqual(eat_tokens("# ifndef "), ["<HASH>", "<SPACE>", "<IDENTIFIER=ifndef>", "<SPACE>"])
        self.assertEqual(eat_tokens("#ifndef 	"), ["<HASH>", "<IDENTIFIER=ifndef>", "<SPACE>", "<TAB>"])
        self.assertEqual(eat_tokens("#ifndef //bla"), ["<HASH>", "<IDENTIFIER=ifndef>", "<SPACE>", "<COMMENT=//bla>"])
        self.assertEqual(eat_tokens("#ifndef//bla "), ["<HASH>", "<IDENTIFIER=ifndef>", "<COMMENT=//bla >"])

    def test_ifdef_keyword(self):
        self.assertEqual(eat_tokens("#ifdef"), ["<HASH>", "<IDENTIFIER=ifdef>"])
        self.assertEqual(eat_tokens("# ifdef "), ["<HASH>", "<SPACE>", "<IDENTIFIER=ifdef>", "<SPACE>"])
        self.assertEqual(eat_tokens("#ifdef 	"), ["<HASH>", "<IDENTIFIER=ifdef>", "<SPACE>", "<TAB>"])
        self.assertEqual(eat_tokens("#ifdef //bla"), ["<HASH>", "<IDENTIFIER=ifdef>", "<SPACE>", "<COMMENT=//bla>"])
        self.assertEqual(eat_tokens("#ifdef//bla "), ["<HASH>", "<IDENTIFIER=ifdef>","<COMMENT=//bla >"])

    def test_include_keyword(self):
        self.assertEqual(eat_tokens("#include"), ["<HASH>", "<IDENTIFIER=include>"])
        self.assertEqual(eat_tokens("# include "), ["<HASH>", "<SPACE>", "<IDENTIFIER=include>", "<SPACE>"])
        self.assertEqual(eat_tokens("#include 	"), ["<HASH>", "<IDENTIFIER=include>", "<SPACE>", "<TAB>"])
        self.assertEqual(eat_tokens("#include //bla"), ["<HASH>", "<IDENTIFIER=include>", "<SPACE>", "<COMMENT=//bla>"])
        self.assertEqual(eat_tokens("#include//bla "), ["<HASH>", "<IDENTIFIER=include>", "<COMMENT=//bla >"])

    def test_pragma_keyword(self):
        self.assertEqual(eat_tokens("#pragma"), ["<HASH>", "<IDENTIFIER=pragma>"])
        self.assertEqual(eat_tokens("# pragma "), ["<HASH>", "<SPACE>", "<IDENTIFIER=pragma>", "<SPACE>"])
        self.assertEqual(eat_tokens("#pragma 	"), ["<HASH>", "<IDENTIFIER=pragma>", "<SPACE>", "<TAB>"])
        self.assertEqual(eat_tokens("#pragma //bla"), ["<HASH>", "<IDENTIFIER=pragma>", "<SPACE>", "<COMMENT=//bla>"])
        self.assertEqual(eat_tokens("#pragma//bla "), ["<HASH>", "<IDENTIFIER=pragma>", "<COMMENT=//bla >"])

    def test_undef_keyword(self):
        self.assertEqual(eat_tokens("#undef"), ["<HASH>", "<IDENTIFIER=undef>"])
        self.assertEqual(eat_tokens("# undef "), ["<HASH>", "<SPACE>", "<IDENTIFIER=undef>", "<SPACE>"])
        self.assertEqual(eat_tokens("#undef 	"), ["<HASH>", "<IDENTIFIER=undef>", "<SPACE>", "<TAB>"])
        self.assertEqual(eat_tokens("#undef //bla"), ["<HASH>", "<IDENTIFIER=undef>", "<SPACE>", "<COMMENT=//bla>"])
        self.assertEqual(eat_tokens("#undef//bla "), ["<HASH>", "<IDENTIFIER=undef>", "<COMMENT=//bla >"])


if __name__ == "__main__":
    unittest.main()
