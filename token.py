class Token:
    def __init__(self, tkn_type, tkn_value, pos, length):
        self.type = str(tkn_type)
        self.value = str(tkn_value)
        self.pos = int(pos)
        self.length = int(length)

    def __repr__(self):
        return '<{self.type}={self.value}>'
