class Token:
    def __init__(self, tkn_type, pos, tkn_value=None):
        self.type = str(tkn_type)
        self.pos = pos
        if tkn_value is not None:
            self.value = str(tkn_value)
            self.length = len(tkn_value)
        else:
            self.value = None
            self.length = 0

    @property
    def line_column(self):
        return self.pos[1]

    def __repr__(self):
        """
        Token representation for debugging, using the format <TYPE=value>
        or simply <TYPE> when value is None
        """
        r = f"<{self.type}={self.value}>" if self.value else f"<{self.type}>"
        return r

    def test(self):
        return self.__repr__()
