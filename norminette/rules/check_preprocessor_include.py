import os.path
import itertools

from norminette.rules import Rule, Check


class CheckPreprocessorInclude(Rule, Check):
    depends_on = (
        "IsPreprocessorStatement",
    )

    def run(self, context):
        """
        Includes must be at the start of the file
        You cannot include anything that isn't an header file
        """
        i = hash_index = context.skip_ws(0)
        i += 1  # skip HASH
        i = context.skip_ws(i)
        if context.check_token(i, "IDENTIFIER") is False:
            return False, 0
        if context.peek_token(i).value != "include":
            return False, 0
        if not self.is_in_start_of_file(context):
            context.new_error("INCLUDE_START_FILE", context.peek_token(hash_index))

        i += 1  # skip INCLUDE
        i = context.skip_ws(i)
        if context.check_token(i, "STRING"):  # "niumxp.h"
            file = context.peek_token(i).value.strip().strip('"')
            file, extension = os.path.splitext(file)
            if extension != ".h":
                context.new_error("INCLUDE_HEADER_ONLY", context.peek_token(i))
        else:  # <niumxp.h>
            less = context.peek_token(i)
            while not context.check_token(i, "MORE_THAN"):
                i += 1
            last = context.peek_token(i - 1)
            prev = context.peek_token(i - 2)
            if last.type != "IDENTIFIER" or not (last.value == "h" and prev.type == "DOT"):
                context.new_error("INCLUDE_HEADER_ONLY", less)

        i += 1  # skip MORE_THAN or STRING

        return True, i

    def is_in_start_of_file(self, context):
        """Check if the include is at the start of the file
        """
        headers = (
            "IsComment",
            "IsEmptyLine",
            "IsPreprocessorStatement",
        )
        history = itertools.filterfalse(lambda item: item in headers, context.history)
        return (
            context.scope.include_allowed
            and next(history, None) is None
        )
