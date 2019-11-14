class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.len = length(source_code)
        self.__char = self.source_code[0]
        self.__pos = 0
        self.__prev_token = None
        self.__token = None


    def peekChar(self):
        return self.__char


    def popChar(self):
        if self.__pos == self.len:
            self.__char - None
        else:
            self.__pos += 1
            self.__char = self.source_code[self.__pos]
            if self.__char == '\\' and self.source_code[self.__pos + 1] == '\\':
                self.__pos += 1


    def peekToken(self):
        return self.__token


    def popToken(self, token):
        self.__prev_token = self.__token
        self.token = token



    def getNextToken(self):
        while True:
            if self.peekChar().isalpha() or self.peekChar() == '_':
                #IDENTIFIER TOKEN
                continue

            elif self.peekChar() == '"':
                #STRING_CONSTANT
                continue

            elif self.peekChar() == '\'':
                #CHARACTER_CONSTANT
                continue

            elif self.peekChar().isnum():
                #NUMERIC CONSTANT token
                continue


            #elif self.peekChar() == IS A COMMENT
                #continue

            #elif self.peekChar() == IS A SYMBOL
                #continue

            elif self.peekChar() == ' ':
                #SPACE
                continue

            elif self.peekChar() == '\t':
                #Tabs
                continue

            elif self.peekChar() == '\n':
                #NEWLINES
                continue

