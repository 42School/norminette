class Token:
    def __init__(self, tkn_type, tkn_value, pos, length):
        self.type = tkn_type
        self.value = tkn_value
        self.pos = pos
        self.length = length

    def __repr__(self):
        return '<{self.type}={self.value}>'
