from smartertodo.lexing.Token import Token


def is_valid(char):
    try:
        char.decode('utf-8')
    except AttributeError:
        return True
    except UnicodeDecodeError:
        return False

    return True


class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.line = 0
        self.index = 0
        self.char = self.text[self.index] if len(self.text) else '\0'

    def advance(self):
        if self.char == '\n':
            self.line += 1

        if self.index < len(self.text) - 1 and self.char != '\0':
            self.index += 1
            self.char = self.text[self.index]

    def peek(self):
        return self.text[min(self.index+1, len(self.text))]

    def get_next_token(self):
        while self.index < len(self.text) - 1 and self.char != '\0':
            if not is_valid(self.char):
                self.skip_invalid()

            if self.char == '/':
                self.advance()
                if self.char == '*':
                    self.advance()
                    return self.lex_c_comment_block()
                elif self.char == '/':
                    return self.lex_comment_block()
            elif self.char == '#':
                return self.lex_comment_block()

            self.advance()

        return Token('EOF', None, self.line, self.index)

    def skip_invalid(self):
        while not is_valid(self.char) and self.index < len(self.text) - 1\
                and self.char != '\0':
            self.advance()

    def lex_comment_block(self):
        text = ''
        comment_type = self.char
        firstchar = self.char
        self.advance
        while firstchar == comment_type and self.char != '\0':
            if self.char != firstchar and self.char != '\n':
                text += self.char

            if self.char == '\n':
                self.advance()
                if firstchar == comment_type:
                    firstchar = self.char
                else:
                    break
            else:
                self.advance()

            if not is_valid(self.char):
                break

        return Token('COMMENT_BLOCK', text, self.line, self.index)

    def lex_c_comment_block(self):
        text = ''
        while self.index < len(self.text) - 1 and self.char != '\0':
            if self.char == '*':
                self.advance()

            text += self.char
            self.advance()
            if self.char == '*' and self.peek() == '/':
                break

        return Token('C_COMMENT_BLOCK', text, self.line, self.index)
