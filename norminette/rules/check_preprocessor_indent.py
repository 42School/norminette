from rules import Rule


class CheckPreprocessorIndent(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsPreprocessorStatement"]

    def run(self, context):
        print ("DEBUG___")
        print (context.tokens[:context.tkn_scope])
#        for t in context.tokens[:context.tkn_scope]:


        return False, 0
