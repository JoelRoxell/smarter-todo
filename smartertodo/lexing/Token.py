class Token(object):
    def __init__(self, token_type, value, line, index):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.index = index
