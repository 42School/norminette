import unittest
import sys
sys.path.append('../..')
from lexer import Lexer

class TokensKeywordsTest(unittest.TestCase):

  def  test_auto_keyword(self):
    self.assertEqual(Lexer("auto").getNextToken().type, "AUTO")
  
  def  test_break_keyword(self):
    self.assertEqual(Lexer("break").getNextToken().type, "BREAK")
  
  def  test_case_keyword(self):
    self.assertEqual(Lexer("case").getNextToken().type, "CASE")

  def  test_char_keyword(self):
    self.assertEqual(Lexer("char").getNextToken().type, "CHAR")

  def  test_const_keyword(self):
    self.assertEqual(Lexer("const").getNextToken().type, "CONST")
  
  def  test_continue_keyword(self):
    self.assertEqual(Lexer("continue").getNextToken().type, "CONTINUE")

  def  test_default_keyword(self):
    self.assertEqual(Lexer("default").getNextToken().type, "DEFAULT")

  def  test_do_keyword(self):
    self.assertEqual(Lexer("do").getNextToken().type, "DO")

  def  test_double_keyword(self):
    self.assertEqual(Lexer("double").getNextToken().type, "DOUBLE")

  def  test_else_keyword(self):
    self.assertEqual(Lexer("else").getNextToken().type, "ELSE")
  
  def  test_enum_keyword(self):
    self.assertEqual(Lexer("enum").getNextToken().type, "ENUM")
  
  def  test_extern_keyword(self):
    self.assertEqual(Lexer("extern").getNextToken().type, "EXTERN")
  
  def  test_float_keyword(self):
    self.assertEqual(Lexer("float").getNextToken().type, "FLOAT")
  
  def  test_for_keyword(self):
    self.assertEqual(Lexer("for").getNextToken().type, "FOR")
  
  def  test_goto_keyword(self):
    self.assertEqual(Lexer("goto").getNextToken().type, "GOTO")

  def  test_if_keyword(self):
    self.assertEqual(Lexer("if").getNextToken().type, "IF")

  def  test_int_keyword(self):
    self.assertEqual(Lexer("int").getNextToken().type, "INT")
  
  def  test_long_keyword(self):
    self.assertEqual(Lexer("long").getNextToken().type, "LONG")
  
  def  test_register_keyword(self):
    self.assertEqual(Lexer("register").getNextToken().type, "REGISTER")

  def  test_return_keyword(self):
    self.assertEqual(Lexer("return").getNextToken().type, "RETURN")

  def  test_signed_keyword(self):
    self.assertEqual(Lexer("signed").getNextToken().type, "SIGNED")
  
  def  test_sizeof_keyword(self):
    self.assertEqual(Lexer("sizeof").getNextToken().type, "SIZEOF")
  
  def  test_static_keyword(self):
    self.assertEqual(Lexer("static").getNextToken().type, "STATIC")

  def  test_struct_keyword(self):
    self.assertEqual(Lexer("struct").getNextToken().type, "STRUCT")

  def  test_switch_keyword(self):
    self.assertEqual(Lexer("switch").getNextToken().type, "SWITCH")
  
  def  test_typedef_keyword(self):
    self.assertEqual(Lexer("typedef").getNextToken().type, "TYPEDEF")
  
  def  test_union_keyword(self):
    self.assertEqual(Lexer("union").getNextToken().type, "UNION")

  def  test_unsigned_keyword(self):
    self.assertEqual(Lexer("unsigned").getNextToken().type, "UNSIGNED")
  
  def  test_void_keyword(self):
    self.assertEqual(Lexer("void").getNextToken().type, "VOID")

  def  test_volatile_keyword(self):
    self.assertEqual(Lexer("volatile").getNextToken().type, "VOLATILE")

  def  test_while_keyword(self):
    self.assertEqual(Lexer("while").getNextToken().type, "WHILE")
  
  def  test_define_keyword(self):
    self.assertEqual(Lexer("define").getNextToken().type, "DEFINE")
  
  def  test_error_keyword(self):
    self.assertEqual(Lexer("error").getNextToken().type, "ERROR")

  def  test_ifndef_keyword(self):
    self.assertEqual(Lexer("ifndef").getNextToken().type, "IFNDEF")

  def  test_ifdef_keyword(self):
    self.assertEqual(Lexer("ifdef").getNextToken().type, "IFDEF")
  
  def  test_include_keyword(self):
    self.assertEqual(Lexer("include").getNextToken().type, "INCLUDE")
  
  def  test_pragma_keyword(self):
    self.assertEqual(Lexer("pragma").getNextToken().type, "PRAGMA")

  def  test_undef_keyword(self):
    self.assertEqual(Lexer("undef").getNextToken().type, "UNDEF")

if __name__ == '__main__':
    unittest.main()