import sys, re
import linecache
from colors import format_output
from Dictionary.keywords import dictionary as keywords
from Dictionary.delimiters import dictionary_assign as dict_assign
from Dictionary.delimiters import dictionary_operator as dict_op
from pprint import pprint


verbose = False
pool = False
debug = False

class Tokenizer:
    #pos is the position of the token in the file, line_pos is it's position in the line
    def __init__(self, type, value, line, pos, line_pos):
        self.type = type
        self.value = value
        self.line = line
        self.pos = pos
        self.line_pos = line_pos
        if debug == True:
            if self.value == '\n':
                print(f"<{self.type}>")
            elif self.value == '\t' or self.value == ' ':
                print(self.value, end="")
            else:
                print(f"<{self.type}=\"{self.value}\"> ", end="")

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.__str__()


class Lexer:

    def __init__(self, source_code):
        self.source_code = source_code
        self.i = 0
        self.current_token = None
        self.line_count = 0
        self.line_pos = 0
        self.list_token = []



    def is_identifier(self, source_code, i):
        j = i
        word = ""
        while source_code[j].isalpha() == True or source_code[j] == '_' or source_code[j].isdigit() == True:
            word += source_code[j]
            j += 1
        if word in keywords:
            self.line_pos = self.i + 1
            self.current_token = Tokenizer(keywords.get(word), word, self.line_count, self.i, self.line_pos)
        else:
            self.line_pos = self.i + 1
            self.current_token = Tokenizer("IDENTIFIER", word, self.line_count, self.i, self.line_pos)
        return j



    def is_space(self, char_space):
        if(char_space == ' '):
            self.line_pos = self.i + 1
            self.current_token = Tokenizer(" ", char_space, self.line_count, self.i, self.line_pos)
        elif (char_space == '\t'):
            self.line_pos = self.i + 1
            self.current_token = Tokenizer("\t", char_space, self.line_count, self.i, self.line_pos)
        elif char_space == '\n':
            self.line_pos = self.i + 1
            self.current_token = Tokenizer("NEW_LINE", char_space, self.line_count, self.i, self.line_pos)



    def is_litteral_string(self, source_code, i):
        j = i + 1
        string = ""
        while source_code[j] != '"':
            if source_code[j] == '\\' and source_code[j + 1] == '"':
                j += 1
            string += source_code[j]
            j += 1
        self.line_pos = self.i + 1
        self.current_token = Tokenizer("STRING_LITTERAL", string, self.line_count, self.i, self.line_pos)
        return j



    def is_char(self, source_code, i):
        j = i + 1
        while source_code[j] != "'":
            if source_code[j] == '\\' and source_code[j + 1] == "'":
                j += 1
            j += 1
        self.line_pos = self.i + 1
        self.current_token = Tokenizer("ONE_CHAR", source_code[j], self.line_count, self.i, self.line_pos)
        return j



    def is_constant(self, source_code, i): 
        j = i
        numbers = ""
        while source_code[j].isdigit() == True:
            numbers += source_code[j]
            j += 1
        self.line_pos = self.i + 1
        self.current_token = Tokenizer("CONSTANT", numbers, self.line_count, self.i, self.line_pos)
        return j - 1



    def is_comment(self, source_code, i):
        j = i
        comment = ""
        token_comment = ""
        if(source_code[j + 1] == '/'):
            # j += 1
            while (source_code[j] != '\n'):
                comment += source_code[j]
                j += 1
            self.line_pos = self.i + 1
            self.current_token = Tokenizer("COMMENT", comment, self.line_count, self.i, self.line_pos)
            """
            on retourne j - 1 pour pouvoir revenir au \n,
            sinon le programme continue, incremente le compteur et "oublie"
            le retour a la ligne.
            """
            return j - 1
        if(source_code[j + 1] == '*'):
            # j += 1
            token_comment = "COMMENT_MULT_START "
            # self.current_token = Tokenizer("COMMENT_MULT_START", "comment debut")
            while(source_code[j:j+2] != "*/"):
                if(source_code[j] == '\n' or source_code[j] == '\t' or source_code[j] == ' '):
                    token_comment += source_code[j]
                    # if source_code[j - 1] == '\n':
                    #     token_comment += "COMMENT_MULT_CURRENT"
                comment += source_code[j]
                j += 1
            if source_code[j:j+2] == "*/":
                token_comment += "COMMENT_MULT_END"
                self.line_pos = self.i + 1
                self.current_token = Tokenizer(token_comment, comment, self.line_count, self.i, self.line_pos)
            return j + 1



    def is_symbol(self, char):
        if char in keywords:
            return True
        else:
            return False



    def is_operator(self, source_code, i):
        j = i
        op = ""
        try:
            while self.is_symbol(source_code[j]) == True:
                op += source_code[j]
                j += 1
            if op in keywords:
                self.line_pos = self.i + 1
                self.current_token = Tokenizer(keywords.get(op), op, self.line_count, self.i, self.line_pos)
            else:
                self.line_pos = self.i + 1
                self.current_token = Tokenizer(op, op, self.line_count, self.i, self.line_pos)
            return j - 1
        except Exception as e:
            print(e)



    def get_next_token(self):
        try:
            """
            on rajoute un retour a la ligne a la fin de mon fichier
            """
#            self.source_code += '\n'
            while self.i < len(self.source_code):
                if self.source_code[:self.i].count("\n"):
                    self.line_count = self.source_code[:self.i].count("\n") + 1
                    # self.line_pos = 0

                if self.source_code[self.i].isalpha() == True or self.source_code[self.i] == '_':
                    self.i = self.is_identifier(self.source_code, self.i) - 1 #IDENTIFIER ou MOT CLE
                    self.list_token.append(self.current_token)

                elif self.source_code[self.i].isspace() == True:
                    self.is_space(self.source_code[self.i])    #GESTION DES ESPACE
                    self.list_token.append(self.current_token)

                elif self.source_code[self.i] == '"':
                    self.i = self.is_litteral_string(self.source_code, self.i) #GESTION DE CHAINE DE CARACTERE
                    self.list_token.append(self.current_token)

                elif self.source_code[self.i] == "'":
                    self.i = self.is_char(self.source_code, self.i) #GESTION DE CARACTERE
                    self.list_token.append(self.current_token)

                elif self.source_code[self.i].isdigit() == True:
                    self.i = self.is_constant(self.source_code, self.i) #GESTION DES CONSTANTE
                    self.list_token.append(self.current_token)

                elif self.source_code[self.i] == '/' and (self.source_code[self.i + 1] == '/' or self.source_code[self.i + 1] == '*'):
                    self.i = self.is_comment(self.source_code, self.i)  #GESTION DE COMMENTAIRE
                    self.list_token.append(self.current_token)

                else:
                    self.i = self.is_operator(self.source_code, self.i)
                    self.list_token.append(self.current_token)

                self.i += 1
        except ValueError:
            print(ValueError)




class Interpreter:
    def __init__(self, list_token):
        self.tab_token = list_token
        self.first_token_line = 0
        self.first_pos_line = 0
        self.error_pos = 0
        self.list_error = []

    def pointer(self, i):
        if self.tab_token[i].type == '*' and self.tab_token[i + 1].type == "IDENTIFIER":
            return True
#        elif self.tab_token[i + 1] == "*":
#            return self.pointer(i + 1)
        return False


    def ope(self, i):
        if self.pointer(i):
            return

    def error(self, token):
        i = self.first_token_line
        line = ""
        while(self.tab_token[i].value != '\n'):
            line += self.tab_token[i].value
            i += 1
        self.list_error.append(f"Invalid Syntax Line: {token.line} Pos: {self.error_pos} line_code: {line}")

    def rules(self):
        i = 0
        while(i != len(self.tab_token)):
            if self.tab_token[i].type == '\n':
                """
                Quand on tombe sur un token de retour a la ligne
                j'initialise un token token_start_line a ma position actuelle + 1
                ce qui me permet de connaitre la position du 1er token de ma nouvelle ligne
                """
                self.first_token_line = i + 1
                self.first_pos_line = self.tab_token[i].pos
            if self.tab_token[i].type in ('+', '-', '%', '/', '*'):
                self.ope(i)
            i += 1



def norm(filename):

    """
    Add a try/except here, check for no such file or no permission execptions
    """
    with open(filename, 'r') as file_code:
        source_code = file_code.read()
    lexer = Lexer(source_code)
    lexer.get_next_token()
    interpreter = Interpreter(lexer.list_token)
    interpreter.rules()
    tab_error = interpreter.list_error
    if len(tab_error) == 0:
        print(format_output(filename + ": OK!", "bold", "green"))
    else:
        print(format_output(filename + ": KO!", "bold", "red"))
        for e in tab_error:
            print("\t" + e)

def main():
    global verbose
    global pool
    global debug

    args = sys.argv
    args.pop(0)

    if '-v' in args:
        verbose = True
        args.pop(args.index('-v'))
    if '-p' in args:
        pool = True
        args.pop(args.index('-p'))
    if '-d' in args:
        debug = True
        args.pop(args.index('-d'))

    for f in args:
        norm(f)

if __name__ == '__main__':
    main()
