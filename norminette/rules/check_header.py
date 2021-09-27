from norminette.rules import Rule
import re

class CheckHeader(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def parse_header(self, context):
        if context.check_token(0, "MULT_COMMENT") is False:
            # print ("Missing or invalid header. Header are being reintroduced as a mandatory part of your files. This is not yet an error.")
            context.new_error("INVALID_HEADER", context.peek_token(0))
            context.header_parsed = True
            return
        context.header += context.peek_token(0).value + '\n'

    def check_header(self, context):
        #val = r"\/\* \*{74} \*\/\n\/\*.*\*\/\n\/\*.*\*\/\n\/\*.{3}([^ ]*).*\*\/\n\/\*.*\*\/\n\/\*   By: ([^ ]*).*\*\/\n\/\*.*\*\/\n\/\*   Created: ([^ ]* [^ ]*) by ([^ ]*).*\*\/\n\/\*   Updated: ([^ ]* [^ ]*) by ([^ ]*).*\*\/\n\/\*.*\*\/\n\/\* \*{74} \*\/\n"
        val_no_check_nl = r"\/\* \*{74} \*\/.\/\*.*\*\/.\/\*.*\*\/.\/\*.{3}([^ ]*).*\*\/.\/\*.*\*\/.\/\*   By: ([^ ]*).*\*\/.\/\*.*\*\/.\/\*   Created: ([^ ]* [^ ]*) by ([^ ]*).*\*\/.\/\*   Updated: ([^ ]* [^ ]*) by ([^ ]*).*\*\/.\/\*.*\*\/.\/\* \*{74} \*\/."

        #correct_header = re.match(val, context.header)
        regex = re.compile(val_no_check_nl, re.DOTALL)
        #correct_header_no_nl = re.match(val_no_check_nl, context.header)
        correct_header_no_nl = regex.search(context.header)
        if correct_header_no_nl is None:
            # print ("Missing or invalid header. Header are being reintroduced as a mandatory part of your files. This is not yet an error.")
            context.new_error("INVALID_HEADER", context.peek_token(0))
        #else:
        #    print (correct_header.group(1,2,3,4,5,6))

    def run(self, context):
        """
            Header checking. Just a warning for now. Does not trigger moulinette error
        """
        if context.header_parsed == True:
            return False, 0
        elif context.history[-1] == "IsComment" and context.header_parsed == False:
            self.parse_header(context)
            context.header_started = True
        elif context.history[-1] != "IsComment" and context.header_started == True:
            self.check_header(context)
            context.header_parsed = True
        elif context.header_started == False and context.header_parsed == False and context.history[-1] != "IsComment":
            context.new_error("INVALID_HEADER", context.peek_token(0))
            # print ("Missing or invalid header. Header are being reintroduced as a mandatory part of your files. This is not yet an error.")
            context.header_parsed = True
