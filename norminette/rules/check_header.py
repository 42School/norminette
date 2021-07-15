from norminette.rules import Rule
import re

class CheckHeader(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []
        self.header_started = False
        self.header_parsed = False
        self.header = ""

    def parse_header(self, context):
        if context.check_token(0, "MULT_COMMENT") is False:
            print ("Missing or invalid header. Header are being reintroduced as a mandatory part of your files. This is not yet an error.")
            self.header_parsed = True
            return
        self.header += context.peek_token(0).value + '\n'

    def check_header(self, context):
        val = r"\/\* \*{74} \*\/\n\/\*.*\*\/\n\/\*.*\*\/\n\/\*.{3}([^ ]*).*\*\/\n\/\*.*\*\/\n\/\*   By: ([^ ]*).*\*\/\n\/\*.*\*\/\n\/\*   Created: ([^ ]* [^ ]*) by ([^ ]*).*\*\/\n\/\*   Updated: ([^ ]* [^ ]*) by ([^ ]*).*\*\/\n\/\*.*\*\/\n\/\* \*{74} \*\/\n"
        correct_header = re.match(val, self.header)
        if correct_header is None:
            pass
            #print ("Missing or invalid header. Header are being reintroduced as a mandatory part of your files. This is not yet an error.")
            #context.new_error("INVALID_HEADER", context.peek_token(0))
        # else:
        #     print (correct_header.group(1,2,3,4,5,6))

    def run(self, context):
        """
        Ternaries are forbidden
        """
        if self.header_parsed == True:
            return False, 0
        elif context.history[-1] == "IsComment" and self.header_parsed == False:
            self.parse_header(context)
            self.header_started = True
        elif context.history[-1] != "IsComment" and self.header_started == True:
            self.check_header(context)
            self.header_parsed = True
        elif self.header_started == False and self.header_parsed == False and context.history[-1] != "IsComment":
            #context.new_error("INVALID_HEADER", context.peek_token(0))
            #print ("Missing or invalid header. Header are being reintroduced as a mandatory part of your files. This is not yet an error.")
            self.header_parsed = True
