from norminette.rules import Rule


allowed_in_header = [
    "IsVarDeclaration",
    "IsUserDefinedType",
    "IsPreprocessorStatement",
    "IsEmptyLine",
    "IsBlockStart",
    "IsBlockEnd",
    "IsComment",
    "IsEndOfLine",
    "IsFuncPrototype",
]

must_be_within_define = [
    "IsVarDeclaration",
    "IsUserDefinedType",
    "IsFuncPrototype",
]


class CheckInHeader(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [
            "IsVarDeclaration",
            "IsUserDefinedType",
            "IsPreprocessorStatement",
            "IsEmptyLine",
            "IsBlockStart",
            "IsBlockEnd",
            "IsComment",
            "IsEndOfLine",
            "IsFuncPrototype",
        ]

    def run(self, context):
        """
        Each .h file must be protected against double inclusion
        Instructions allowed in header files:
            - Variable declaration
            - User defined types
            - Comments
            - Function prototypes
        """
        if context.filetype != "h":
            return False, 0
        sc = context.scope
        while sc.name != "GlobalScope":
            sc = sc.get_outer()
        if context.history[-1] not in allowed_in_header:
            context.new_error("FORBIDDEN_IN_HEADER", context.peek_token(0))
            return False, 0
        elif context.history[-1] in must_be_within_define and sc.header_protection != 1:
            context.new_error("HEADER_PROT_ALL", context.peek_token(0))
        return False, 0
