from smartertodo.lexing.Lexer import Lexer
from smartertodo.lexing.Token import TokenType
import os


def get_comments_from_text(text):
    lexer = Lexer(text)
    token = lexer.get_next_token()
    tokens = [token] if token.token_type == TokenType.COMMENT else []

    while token.token_type != TokenType.EOF:
        token = lexer.get_next_token()

        if token.token_type == TokenType.COMMENT:
            tokens.append(token)

    return tokens


def get_comments_from_directory(directory, print_directories=False):
    comments = []
    for root, subdirs, files in os.walk(directory):
        for filename in files:
            dirname = os.path.join(root, filename)

            if print_directories:
                print(dirname)

            comments = comments + get_comments_from_text(
                open(dirname).read())

    return comments
