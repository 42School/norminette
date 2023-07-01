import sys
import contextlib

from norminette.rules import PrimaryRule
from norminette.exceptions import CParsingError

UNARY_OPERATORS = (
    "PLUS",
    "MINUS",
    "NOT",  # !
    "BWISE_NOT",  # ~
)

BINARY_OPERATORS = (
    # Arithmetic operators
    "PLUS",
    "MINUS",
    "MULT",
    "DIV",
    "MODULO",
    # Relational operators
    "EQUALS",  # ==
    "NOT_EQUAL",  # !=
    "MORE_THAN",  # > (why not GREATER_THAN?)
    "LESS_THAN",  # <
    "GREATER_OR_EQUAL",  # >=
    "LESS_OR_EQUAL",  # <=
    # Logical operators
    "AND",
    "OR",
    # Bitwise operators
    "BWISE_AND",  # &
    "BWISE_OR",  # |
    "BWISE_XOR",  # ^
    "BWISE_XOR",  # ^
    "LEFT_SHIFT",  # << (why not BWISE_LEFT?)
    "RIGHT_SHIFT",  # >>
)


@contextlib.contextmanager
def recursion_limit(limit):
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(limit)
    yield
    sys.setrecursionlimit(old_limit)


class IsPreprocessorStatement(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 100
        self.scope = []

    def run(self, context):
        """
        Catches any kind of preprocessor statements
        Handles indentation related informations
        """
        i = context.skip_ws(0)
        if not context.check_token(i, "HASH"):
            return False, 0
        i = context.skip_ws(i + 1)
        if context.check_token(i, "NEWLINE"):  # Null directive
            return True, i + 1                 # TODO: Fix null directives
        # Why `if` and `else` need to be a special case?
        if not context.check_token(i, ("IDENTIFIER", "IF", "ELSE")):
            raise CParsingError(f"Invalid preprocessor statement {context.peek_token(i)}")
        token = context.peek_token(i)
        direc = (token.value if token.type == "IDENTIFIER" else token.type).lower()
        i += 1
        i = context.skip_ws(i)
        if checker := getattr(self, f"check_{direc}", None):
            return checker(context, i)
        raise CParsingError(f"Invalid preprocessing directive #{direc}")

    def check_define(self, context, index):
        pass

    def check_import(self, context, index):
        pass

    def check_pragma(self, context, index):
        return self._just_token_string("pragma", context, index)

    def check_error(self, context, index):
        return self._just_token_string("error", context, index)

    def check_warning(self, context, index):
        return self._just_token_string("warning", context, index)

    def check_if(self, context, index):
        context.preproc_scope_indent += 1
        return self._just_constant_expression("if", context, index)

    def check_elif(self, context, index):
        context.preproc_scope_indent += 1
        return self._just_constant_expression("elif", context, index)

    def check_ifdef(self, context, index):
        context.preproc_scope_indent += 1
        return self._just_identifier("ifdef", context, index)

    def check_ifndef(self, context, index):
        context.preproc_scope_indent += 1
        return self._just_identifier("infdef", context, index)

    def check_undef(self, context, index):
        return self._just_identifier("undef", context, index)

    def check_else(self, context, index):
        if context.preproc_scope_indent == 0:  # This need to be an error or a warning?
            raise CParsingError("#else directive without matching #if or #elif")
        context.preproc_scope_indent += 1
        return self._just_eol("else", context, index)

    def check_endif(self, context, index):
        if context.preproc_scope_indent == 0:  # This need to be an error or a warning?
            raise CParsingError("#endif directive without matching #if, #elif or #else")
        context.preproc_scope_indent -= 1
        return self._just_eol("endif", context, index)

    def check_include(self, context, index):
        def check_include_header():
            """Checks the argument of an include statement.

            Examples of valid headers:
            - `"libft.h"`
            - `<    bla.h   >`
            - `<42.h   >`
            - `<   four.two>`
            """
            nonlocal context, index
            if context.check_token(index, "STRING"):
                index += 1
                return True, index
            if not context.check_token(index, "LESS_THAN"):
                return False, index
            index = context.skip_ws(index + 1)
            if not context.check_token(index, "IDENTIFIER"):
                return False, index
            # TODO: Add to support `sys/types/a/b/c/`
            index += 1
            if not context.check_token(index, "DOT"):
                return False, index
            index += 1
            if not context.check_token(index, "IDENTIFIER"):  # We need check if is 'h'?
                return False, index
            index = context.skip_ws(index + 1)
            if not context.check_token(index, "MORE_THAN"):
                return False, index
            index += 1
            return True, index

        is_valid_argument, index = check_include_header()
        if not is_valid_argument:
            raise CParsingError("Invalid argument for #include directive")
        index = context.skip_ws(index)
        return self._just_eol("include", context, index)

    def _just_token_string(self, directive, context, index):
        if context.check_token(index, "NEWLINE"):
            index += 1
            return True, index
        lines = 1
        while context.peek_token(index) is not None and lines > 0:
            if context.check_token(index, "NEWLINE"):
                lines -= 1
            elif context.check_token(index, "BACKSLASH"):
                lines += 1
            index += 1
        if lines > 0:
            raise CParsingError(f"Unexpected end of file after #{directive} directive")
        return True, index

    def _just_constant_expression(self, directive, context, index):
        parser = ConstantExpressionParser(context, index)
        return parser.parse()

    def _just_identifier(self, directive, context, index):
        if not context.check_token(index, "IDENTIFIER"):
            raise CParsingError(f"Invalid argument for #{directive} statement")
        index += 1
        return self._just_eol(directive, context, index)

    def _just_eol(self, directive, context, index):
        index = context.skip_ws(index)
        if context.peek_token(index) is None:
            raise CParsingError(f"Unexpected end of file after #{directive} directive")
        if not context.check_token(index, "NEWLINE"):
            raise CParsingError(f"Extra tokens at end of #{directive} directive")
        index += 1
        return True, index


class ConstantExpressionParser:
    """Parses a constant expression that can be used in preprocessor statements.

    ```bnf
    <expression> ::= <term>
            | unary_operator <expression>
            | ( "(" <expression> ")" | <expression> ) ( binary_operator <expression> )*
    <term> ::= string
            | constant
            | identifier
            | identifier '(' [ <expression> ("," <expression> )* ] ')'
    ```
    The `string`, `constant` and `identifier` comes from the tokenizer.
    """

    def __init__(self, context, index):
        self.context = context
        self.index = index

    def parse(self) -> tuple[bool, int]:
        try:
            self.parse_constant_expression()
            if self.context.peek_token(self.index) is None:
                raise CParsingError("Unexpected end of file")
            if not self.context.check_token(self.index, "NEWLINE"):
                print(self.context.tokens[self.index:])
                raise CParsingError("Unexpected tokens after the constant expression")
            self.index += 1  # Skip the newline
        except RecursionError:
            raise CParsingError("Constant expression too complex")
        return True, self.index

    def skip_ws(self) -> None:
        self.index = self.context.skip_ws(self.index)

    @recursion_limit(100)
    def parse_constant_expression(self) -> None:
        self.parse_expression()

    def parse_expression(self) -> None:
        if self.context.check_token(self.index, "LPARENTHESIS"):
            self.index += 1
            self.parse_expression()
            if not self.context.check_token(self.index, "RPARENTHESIS"):
                raise CParsingError("Missing closing parenthesis while parsing constant expression")
            self.index += 1
            self.parse_potential_binary_operator()
            return

        if self.context.check_token(self.index, UNARY_OPERATORS):
            self.index += 1
            self.parse_expression()
            return

        if self.context.check_token(self.index, "IDENTIFIER"):
            self.index += 1
            if self.context.check_token(self.index, "LPARENTHESIS"):
                self.index += 1
                self.parse_function_macro()
                return
            self.parse_potential_binary_operator()
            return

        if self.context.check_token(self.index, ("STRING", "CONSTANT")):
            self.index += 1
            self.parse_potential_binary_operator()
            return

        raise CParsingError(f"Unexpected token: {self.context.peek_token(self.index)}")

    def parse_function_macro(self) -> None:
        self.skip_ws()
        if not self.context.check_token(self.index, "RPARENTHESIS"):
            self.parse_expression()
            while self.context.check_token(self.index, "COMMA"):
                self.index += 1
                self.skip_ws()
                self.parse_expression()
        if not self.context.check_token(self.index, "RPARENTHESIS"):
            raise CParsingError("Missing closing parenthesis")
        self.index += 1
        self.skip_ws()

    def parse_potential_binary_operator(self) -> None:
        self.skip_ws()
        if self.context.check_token(self.index, BINARY_OPERATORS):
            self.index += 1
            self.skip_ws()
            self.parse_expression()
            return
