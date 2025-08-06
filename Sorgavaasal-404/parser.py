class Node:
    pass

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

class StringNode(Node):
    def __init__(self, value):
        self.value = value

class VarAssignNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarAccessNode(Node):
    def __init__(self, name):
        self.name = name

class PrintNode(Node):
    def __init__(self, value):
        self.value = value

class ReturnNode(Node):
    def __init__(self, value):
        self.value = value

class FunctionDefNode(Node):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class FunctionCallNode(Node):
    def __init__(self, name):
        self.name = name

def parse(tokens):
    pos = 0
    statements = []

    def current():
        return tokens[pos] if pos < len(tokens) else None

    def eat(type_=None, value=None):
        nonlocal pos
        tok = current()
        if not tok:
            raise Exception("Unexpected end of input")
        if type_ and tok.type != type_:
            raise Exception(f"Expected {type_}, got {tok.type}")
        if value and tok.value != value:
            raise Exception(f"Expected {value}, got {tok.value}")
        pos += 1
        return tok

    while pos < len(tokens):
        tok = current()
        if tok.type == "KEYWORD" and tok.value == "kooptaVaran":
            eat("KEYWORD", "kooptaVaran")
            name = eat("IDENTIFIER").value
            eat("SYMBOL", ":")
            body = []
            while current() and current().value != "thirumbaVaa":
                body.append(parse([eat()])[0])
            eat("KEYWORD", "thirumbaVaa")
            statements.append(FunctionDefNode(name, body))

        elif tok.type == "IDENTIFIER":
            name = eat("IDENTIFIER").value
            eat("SYMBOL", "=")
            val_token = eat()
            if val_token.type == "NUMBER":
                value = NumberNode(val_token.value)
            elif val_token.type == "STRING":
                value = StringNode(val_token.value)
            else:
                value = VarAccessNode(val_token.value)
            statements.append(VarAssignNode(name, value))

        elif tok.type == "KEYWORD" and tok.value == "Vandhutann":
            eat("KEYWORD", "Vandhutann")
            val_token = eat()
            value = NumberNode(val_token.value) if val_token.type == "NUMBER" else VarAccessNode(val_token.value)
            statements.append(ReturnNode(value))

        elif tok.type == "IDENTIFIER":
            name = eat("IDENTIFIER").value
            statements.append(FunctionCallNode(name))

        else:
            raise Exception(f"Unexpected token: {tok}")
    return statements
