# dialogue.py

import sys
import operator

# === Token Definitions ===

class Token:
    SAY = 'solra'
    CALC = 'CALC'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    SEMICOLON = 'SEMICOLON'
    EOF = 'EOF'

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'


# === Lexer / Tokenizer ===

def tokenize(code):
    tokens = []
    i = 0
    while i < len(code):
        if code[i].isspace():
            i += 1
            continue
        if code.startswith('solra', i):
            tokens.append(Token(Token.SAY))
            i += 3
            continue
        if code.startswith('calc', i):
            tokens.append(Token(Token.CALC))
            i += 4
            continue
        if code[i] == '"':
            i += 1
            start = i
            while i < len(code) and code[i] != '"':
                i += 1
            tokens.append(Token(Token.STRING, code[start:i]))
            i += 1
            continue
        if code[i].isdigit():
            start = i
            while i < len(code) and (code[i].isdigit() or code[i] == '.'):
                i += 1
            tokens.append(Token(Token.NUMBER, float(code[start:i])))
            continue
        if code[i] in '+-*/':
            tokens.append(Token(Token.OPERATOR, code[i]))
            i += 1
            continue
        if code[i] == ';':
            tokens.append(Token(Token.SEMICOLON))
            i += 1
            continue
        i += 1  # skip unknowns
    tokens.append(Token(Token.EOF))
    return tokens


# === AST Nodes ===

class SayNode:
    def __init__(self, text):
        self.text = text

    def eval(self):
        print(self.text)


class CalcNode:
    def __init__(self, expression):
        self.expression = expression  # list of tokens

    def eval(self):
        result = evaluate_expression(self.expression)
        print(result)


# === Expression Evaluator ===

def evaluate_expression(tokens):
    # Convert tokens to RPN using Shunting Yard
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    ops = []

    for token in tokens:
        if token.type == Token.NUMBER:
            output.append(token.value)
        elif token.type == Token.OPERATOR:
            while (ops and ops[-1] != '(' and
                   precedence[ops[-1]] >= precedence[token.value]):
                output.append(ops.pop())
            ops.append(token.value)

    while ops:
        output.append(ops.pop())

    # Evaluate RPN
    stack = []
    ops_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    for item in output:
        if isinstance(item, float):
            stack.append(item)
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops_map[item](a, b))

    return stack[0]


# === Parser ===

def parse(tokens):
    i = 0
    ast = []

    while i < len(tokens):
        if tokens[i].type == Token.SAY:
            if tokens[i+1].type == Token.STRING and tokens[i+2].type == Token.SEMICOLON:
                ast.append(SayNode(tokens[i+1].value))
                i += 3
            else:
                raise SyntaxError("Invalid 'say' syntax")
        elif tokens[i].type == Token.CALC:
            expr_tokens = []
            i += 1
            while tokens[i].type != Token.SEMICOLON and tokens[i].type != Token.EOF:
                expr_tokens.append(tokens[i])
                i += 1
            if tokens[i].type != Token.SEMICOLON:
                raise SyntaxError("Missing semicolon after 'calc'")
            ast.append(CalcNode(expr_tokens))
            i += 1
        elif tokens[i].type == Token.EOF:
            break
        else:
            i += 1
    return ast


# === Interpreter ===

def interpret(ast):
    for node in ast:
        node.eval()


# === File + CLI Support ===

def run_file(filename):
    try:
        with open(filename, 'r') as f:
            code = f.read()
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast)
    except Exception as e:
        print("Error:", e)


def run_cli(args):
    if args[0] == 'solra':
        text = ' '.join(args[1:])
        SayNode(text).eval()
    elif args[0] == 'calc':
        code = ' '.join(args) + ';'
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast)
    else:
        print("Usage:\n  python dialogue.py say \"Hello\"\n  python dialogue.py calc 5 + 10 * 2")


# === Main ===

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_cli(sys.argv[1:])
    else:
        run_file('sample.dlg')
