identifiers = [
    "CHAR",
    "DOUBLE",
    "ENUM",
    "FLOAT",
    "INT",
    "LONG",
    "SHORT",
    "UNION",
    "VOID",
    "IDENTIFIER"
]

specifiers = [
    "CONST",
    "REGISTER",
    "STATIC",
    "STRUCT",
    # "OP_MULT",
    "VOLATILE"
]

size_specifiers = [
    "LONG",
    "SHORT"
]

sign_specifiers = [
    "SIGNED",
    "UNSIGNED"
]


class checkFuncDeclaration:
    def __init__(self):
        self.name = "CheckFuncDeclaration"

    def checkLine(line):
        s = """
        func declaration can be made of :
            (
                (
                    ((?[sign_specifiers]?)+[size_specifiers]+(?(LONG|INT)?))
                    |([size_specifiers]+(DOUBLE))
                    |([identifiers])
                )
                +(OP_MULT{0,})
                +IDENTIFIER+OPENING_PARENTHESIS
                +(?
                    (
                        ((
                        ((?[sign_specifiers]?)+[size_specifiers]+(?(LONG|INT)?))
                        |([size_specifiers]+(DOUBLE))
                        |([identifiers])
                        +(OP_MULT{0,})+IDENTIFIER){1,})
                        +(
                            (
                                (OP_COMMA)+
                                (
                                    (
                                        (?[sign_specifiers]?)
                                        +[size_specifiers]
                                        +(?(LONG|INT)?)
                                    )
                                    |([size_specifiers]+(DOUBLE))
                                    |([identifiers])
                                )+(OP_MULT{0,})+IDENTIFIER
                            ){0,}
                        )
                    )
                    |
                    VOID
                ?)
                +CLOSING_PARENTHESIS+(?OP_SEMI_COLON?)+NEWLINE
            )
        """
        for tkn in line:
            pass

    def run(tokens):
        line = []
        for tkn in tokens:
            if tkn.type is "NEWLINE":
                """Parse the line and check if it's a function declaration
                or prototype, is so apply the rules to it
                """
                pass
            else:
                line.append(tkn)
