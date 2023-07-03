import itertools
from pathlib import Path

from norminette.rules import Rule


class CheckPreprocessorProtection(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = [
            "IsPreprocessorStatement",
        ]

    def run(self, context):
        """
        Header protection must be as follows:
        ```c
        #ifndef __FILENAME_H__
        # define __FILENAME_H__
        #endif
        ```
        Any header instruction must be within the header protection
        """
        if context.filetype != "h":
            return False, 0
        i = context.skip_ws(0)
        hash = context.peek_token(i)
        i += 1  # Skip the HASH
        i = context.skip_ws(i)
        if not context.check_token(i, "IDENTIFIER"):
            return False, 0
        # TODO: Add to check if macro definition is bellow #ifndef
        t = context.peek_token(i)
        if not t or t.type != "IDENTIFIER" or t.value.upper() not in ("IFNDEF", "ENDIF"):
            return False, 0
        i += 1
        if t.value.upper() == "ENDIF":
            if context.preproc.indent == 0:
                i = context.skip_ws(i, nl=True, comment=True)
                if context.peek_token(i) is not None:
                    context.new_error("HEADER_PROT_ALL_AF", context.peek_token(i))
            return False, 0
        if context.preproc.indent != 1:
            return False, 0
        i = context.skip_ws(i)
        macro = context.peek_token(i).value
        guard = Path(context.filename).name.upper().replace(".", "_")
        if macro != guard:
            if macro.upper() == guard:
                context.new_error("HEADER_PROT_UPPER", context.peek_token(i))
            else:
                context.new_error("HEADER_PROT_NAME", context.peek_token(i))
        else:
            headers = (
                "IsComment",
                "IsEmptyLine",
            )
            history = itertools.filterfalse(lambda item: item in headers, context.history)
            if next(history, None):
                # We can't say what line contains the instruction outside
                # header protection due to limited history information.
                context.new_error("HEADER_PROT_ALL", hash)
        return False, 0
