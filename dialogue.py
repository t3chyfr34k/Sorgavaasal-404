# dialogue.py

import sys

class Token:
    SAY = 'SAY'
    STRING = 'STRING'
    SEMICOLON = 'SEMICOLON'
    EOF = 'EOF'

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'


def tokenize(code):
    tokens = []
    i = 0
    while i < len(code):
        if code[i].isspace():
            i += 1
            continue
        if code.startswith('say', i):
            tokens.append(Token(Token.SAY))
            i += 3
            continue
        if code[i] == '"':
            i += 1
            start = i
            while i < len(code) and code[i] != '"':
                i += 1
            tokens.append(Token(Token.STRING, code[start:i]))
            i += 1  # skip closing quote
            continue
        if code[i] == ';':
            tokens.append(Token(Token.SEMICOLON))
            i += 1
            continue
        i += 1  # skip unknown characters
    tokens.append(Token(Token.EOF))
    return tokens


class SayNode:
    def __init__(self, text):
        self.text = text

    def eval(self):
        print(self.text)


def parse(tokens):
    i = 0
    ast = []
    while i < len(tokens):
        if tokens[i].type == Token.SAY:
            if (i + 2 < len(tokens) and
                tokens[i + 1].type == Token.STRING and
                tokens[i + 2].type == Token.SEMICOLON):
                ast.append(SayNode(tokens[i + 1].value))
                i += 3
            else:
                raise SyntaxError('Invalid syntax near say statement')
        elif tokens[i].type == Token.EOF:
            break
        else:
            i += 1
    return ast


def interpret(ast):
    for node in ast:
        node.eval()


def run_file(filename):
    try:
        with open(filename, 'r') as f:
            code = f.read()
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")


def run_cli(args):
    if args[0] != 'say':
        print("Error: Unknown command. Try: python dialogue.py say \"Hello World\"")
        return
    text = ' '.join(args[1:])
    node = SayNode(text)
    node.eval()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_cli(sys.argv[1:])
    else:
        run_file('sample.dlg')
