class Node:
    pass

class FunctionNode(Node):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class AssignNode(Node):
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

class ReturnNode(Node):
    def __init__(self, value):
        self.value = value

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class VarNode(Node):
    def __init__(self, name):
        self.name = name

class NumNode(Node):
    def __init__(self, value):
        self.value = int(value)

def parse(tokens):
    pos = 0
    def expect(type_):
        nonlocal pos
        if pos < len(tokens) and tokens[pos][0] == type_:
            tok = tokens[pos]
            pos += 1
            return tok
        raise SyntaxError(f"Expected {type_}, got {tokens[pos]}")

    def parse_expression():
        left = parse_term()
        while pos < len(tokens) and tokens[pos][0] == 'PLUS':
            expect('PLUS')
            right = parse_term()
            left = BinOpNode(left, '+', right)
        return left

    def parse_term():
        tok = tokens[pos]
        if tok[0] == 'NUMBER':
            expect('NUMBER')
            return NumNode(tok[1])
        elif tok[0] == 'IDENT':
            expect('IDENT')
            return VarNode(tok[1])
        else:
            raise SyntaxError("Invalid term")

    def parse_statement():
        if tokens[pos][0] == 'NUMBER_TYPE':
            expect('NUMBER_TYPE')
            varname = expect('IDENT')[1]
            expect('ASSIGN')
            expr = parse_expression()
            expect('SEMICOLON')
            return AssignNode(varname, expr)
        elif tokens[pos][0] == 'RETURN':
            expect('RETURN')
            expr = parse_expression()
            expect('SEMICOLON')
            return ReturnNode(expr)
        else:
            raise SyntaxError("Invalid statement")

    def parse_function():
        expect('FUNCTION')
        name = expect('IDENT')[1]
        expect('LPAREN')
        expect('RPAREN')
        expect('LBRACE')
        body = []
        while tokens[pos][0] != 'RBRACE':
            body.append(parse_statement())
        expect('RBRACE')
        return FunctionNode(name, body)

    return parse_function()
