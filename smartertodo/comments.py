from smartertodo.lexing.Lexer import Lexer
import os


def get_comments_from_text(text):
    lexer = Lexer(text)
    token = lexer.get_next_token()
    tokens = [token] if 'comment' in token.token_type.lower() else []

    while token.token_type != 'EOF':
        token = lexer.get_next_token()

        if 'comment' in token.token_type.lower():
            tokens.append(token)

    return tokens


def get_comments_from_directory(directory):
    comments = []
    for root, subdirs, files in os.walk(directory):
        for filename in files:
            comments = comments + get_comments_from_text(
                open(os.path.join(root, filename)).read())

    return comments
