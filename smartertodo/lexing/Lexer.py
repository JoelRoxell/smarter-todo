from smartertodo.lexing.Token import Token, TokenType


def is_valid(char):
    '''
    Check if a char / string is good.
    '''
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
        '''
        Go to next character.
        '''
        if self.char == '\n':
            self.line += 1

        if self.index < len(self.text) - 1:
            self.index += 1
            self.char = self.text[self.index]
        else:
            self.char = '\0'

    def peek(self):
        '''
        Used to check what the next character is without advancing.
        '''
        return self.text[min(self.index+1, len(self.text))]

    def get_next_token(self):
        '''
        Get the next token of the text
        '''
        while self.index < len(self.text) - 1 and self.char != '\0':
            # We currently dont care about none-utf8 characters.
            # Without this check, the program might get stuck if it is
            # going through a let's say binary file.
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

        return Token(TokenType.EOF, None, self.line, self.index)

    def skip_invalid(self):
        '''
        Skips invalid characters
        '''
        while not is_valid(self.char) and self.index < len(self.text) - 1\
                and self.char != '\0':
            self.advance()

    def lex_comment_block(self):
        '''
        Parses // comments and # comments
        '''
        text = ''
        comment_type = self.char
        firstchar = self.char
        self.advance()
        while firstchar == comment_type and self.char != '\0':
            if not is_valid(self.char):
                break

            if self.char != firstchar:
                text += self.char

            if self.char == '\n':
                self.advance()

                # check if the starting character of the new line
                # is the same as the comment block started with.
                # otherwise, the comment has reached its end.
                if firstchar == comment_type:
                    firstchar = self.char
                else:
                    break
            else:
                self.advance()

        return Token(TokenType.COMMENT, text, self.line, self.index)

    def lex_c_comment_block(self):
        '''
        Parses /* */ comments
        '''
        text = ''
        while self.index < len(self.text) - 1 and self.char != '\0':
            if self.char == '*':
                self.advance()

            text += self.char
            self.advance()
            if self.char == '*' and self.peek() == '/':
                break

        return Token(TokenType.COMMENT, text, self.line, self.index)
