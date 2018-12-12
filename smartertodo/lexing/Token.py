class TokenType:
    EOF = 0
    COMMENT = 1


class Token(object):
    def __init__(self, token_type, value, line, index):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.index = index
